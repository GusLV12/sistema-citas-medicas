from django.db import migrations

SQL = """
CREATE OR REPLACE FUNCTION accounts_set_updated_at() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$;
CREATE OR REPLACE FUNCTION accounts_require_profile_role() RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE account_role varchar;
BEGIN
  SELECT role INTO account_role FROM accounts_user WHERE id = NEW.user_id FOR KEY SHARE;
  IF account_role <> TG_ARGV[0] THEN RAISE EXCEPTION 'Profile role does not match user role'; END IF;
  RETURN NEW;
END; $$;
CREATE OR REPLACE FUNCTION accounts_prevent_profile_role_change() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.role <> OLD.role AND (
    (EXISTS (SELECT 1 FROM accounts_patient WHERE user_id = NEW.id) AND NEW.role <> 'patient') OR
    (EXISTS (SELECT 1 FROM accounts_doctor WHERE user_id = NEW.id) AND NEW.role <> 'doctor')
  ) THEN RAISE EXCEPTION 'A user role cannot change while it owns a profile'; END IF;
  RETURN NEW;
END; $$;
CREATE TRIGGER accounts_user_updated BEFORE UPDATE ON accounts_user FOR EACH ROW EXECUTE FUNCTION accounts_set_updated_at();
CREATE TRIGGER accounts_patient_updated BEFORE UPDATE ON accounts_patient FOR EACH ROW EXECUTE FUNCTION accounts_set_updated_at();
CREATE TRIGGER accounts_doctor_updated BEFORE UPDATE ON accounts_doctor FOR EACH ROW EXECUTE FUNCTION accounts_set_updated_at();
CREATE TRIGGER accounts_patient_role BEFORE INSERT OR UPDATE OF user_id ON accounts_patient FOR EACH ROW EXECUTE FUNCTION accounts_require_profile_role('patient');
CREATE TRIGGER accounts_doctor_role BEFORE INSERT OR UPDATE OF user_id ON accounts_doctor FOR EACH ROW EXECUTE FUNCTION accounts_require_profile_role('doctor');
CREATE TRIGGER accounts_user_role BEFORE UPDATE OF role ON accounts_user FOR EACH ROW EXECUTE FUNCTION accounts_prevent_profile_role_change();
"""

class Migration(migrations.Migration):
    dependencies = [("accounts", "0001_initial")]
    operations = [migrations.RunSQL(SQL, migrations.RunSQL.noop)]
