from django.db import migrations

SQL = """
CREATE OR REPLACE FUNCTION consultations_set_updated_at() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$;
CREATE OR REPLACE FUNCTION consultations_require_completed_appointment() RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE current_status varchar;
BEGIN
  SELECT status INTO current_status FROM scheduling_appointment WHERE id = NEW.appointment_id FOR UPDATE;
  IF current_status <> 'completed' THEN RAISE EXCEPTION 'A consultation requires a completed appointment'; END IF;
  RETURN NEW;
END; $$;
CREATE TRIGGER consultations_updated BEFORE UPDATE ON consultations_consultation FOR EACH ROW EXECUTE FUNCTION consultations_set_updated_at();
CREATE TRIGGER consultations_completed BEFORE INSERT OR UPDATE OF appointment_id ON consultations_consultation FOR EACH ROW EXECUTE FUNCTION consultations_require_completed_appointment();
"""

class Migration(migrations.Migration):
    dependencies = [("consultations", "0001_initial"), ("scheduling", "0002_postgresql_integrity")]
    operations = [migrations.RunSQL(SQL, migrations.RunSQL.noop)]
