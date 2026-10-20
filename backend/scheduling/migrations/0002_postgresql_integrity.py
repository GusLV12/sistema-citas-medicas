from django.db import migrations

SQL = """
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER TABLE catalogs_consultingroom ADD CONSTRAINT consulting_room_id_clinic_unique UNIQUE (id, clinic_id);
ALTER TABLE scheduling_appointment ADD COLUMN time_range TSTZRANGE GENERATED ALWAYS AS (tstzrange(starts_at, ends_at, '[)')) STORED;
ALTER TABLE scheduling_appointment
  ADD CONSTRAINT appointment_doctor_clinic_fk FOREIGN KEY (doctor_id, clinic_id)
  REFERENCES catalogs_doctorclinic (doctor_id, clinic_id) ON DELETE RESTRICT,
  ADD CONSTRAINT appointment_doctor_specialty_fk FOREIGN KEY (doctor_id, specialty_id)
  REFERENCES catalogs_doctorspecialty (doctor_id, specialty_id) ON DELETE RESTRICT,
  ADD CONSTRAINT appointment_room_clinic_fk FOREIGN KEY (consulting_room_id, clinic_id)
  REFERENCES catalogs_consultingroom (id, clinic_id) ON DELETE RESTRICT;
ALTER TABLE scheduling_appointment ADD CONSTRAINT appointment_no_doctor_overlap
  EXCLUDE USING gist (doctor_id WITH =, time_range WITH &&) WHERE (status IN ('pending', 'confirmed'));
ALTER TABLE scheduling_appointment ADD CONSTRAINT appointment_no_patient_overlap
  EXCLUDE USING gist (patient_id WITH =, time_range WITH &&) WHERE (status IN ('pending', 'confirmed'));
ALTER TABLE scheduling_appointment ADD CONSTRAINT appointment_no_room_overlap
  EXCLUDE USING gist (consulting_room_id WITH =, time_range WITH &&)
  WHERE (consulting_room_id IS NOT NULL AND status IN ('pending', 'confirmed'));
CREATE OR REPLACE FUNCTION scheduling_set_updated_at() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$;
CREATE TRIGGER scheduling_appointment_updated BEFORE UPDATE ON scheduling_appointment FOR EACH ROW EXECUTE FUNCTION scheduling_set_updated_at();
CREATE TRIGGER scheduling_specialty_updated BEFORE UPDATE ON catalogs_specialty FOR EACH ROW EXECUTE FUNCTION scheduling_set_updated_at();
CREATE TRIGGER scheduling_clinic_updated BEFORE UPDATE ON catalogs_clinic FOR EACH ROW EXECUTE FUNCTION scheduling_set_updated_at();
CREATE TRIGGER scheduling_room_updated BEFORE UPDATE ON catalogs_consultingroom FOR EACH ROW EXECUTE FUNCTION scheduling_set_updated_at();
CREATE TRIGGER scheduling_availability_updated BEFORE UPDATE ON catalogs_availabilityrule FOR EACH ROW EXECUTE FUNCTION scheduling_set_updated_at();
"""

class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_postgresql_guards"),
        ("catalogs", "0001_initial"),
        ("scheduling", "0001_initial"),
    ]
    operations = [migrations.RunSQL(SQL, migrations.RunSQL.noop)]
