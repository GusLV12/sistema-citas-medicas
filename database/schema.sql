-- Sistema de citas médicas
-- Esquema inicial para PostgreSQL 14 o superior.
-- Las notas clínicas requieren controles de acceso adicionales en la aplicación.

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TYPE user_role AS ENUM ('admin', 'patient', 'doctor');
CREATE TYPE appointment_status AS ENUM (
    'pending',
    'confirmed',
    'cancelled',
    'completed',
    'no_show',
    'rescheduled'
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role user_role NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT users_email_not_blank CHECK (btrim(email) <> '')
);

CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE RESTRICT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(30),
    birth_date DATE,
    emergency_contact_name VARCHAR(200),
    emergency_contact_phone VARCHAR(30),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT patients_name_not_blank CHECK (
        btrim(first_name) <> '' AND btrim(last_name) <> ''
    )
);

CREATE TABLE doctors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE RESTRICT,
    license_number VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    default_appointment_minutes SMALLINT NOT NULL DEFAULT 30,
    biography TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT doctors_name_not_blank CHECK (
        btrim(first_name) <> '' AND btrim(last_name) <> ''
    ),
    CONSTRAINT doctors_duration_positive CHECK (
        default_appointment_minutes BETWEEN 5 AND 240
    )
);

CREATE TABLE specialties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(120) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT specialties_name_not_blank CHECK (btrim(name) <> '')
);

CREATE TABLE clinics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(160) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(30),
    timezone VARCHAR(64) NOT NULL DEFAULT 'America/Mexico_City',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT clinics_name_not_blank CHECK (btrim(name) <> ''),
    CONSTRAINT clinics_address_not_blank CHECK (btrim(address) <> '')
);

CREATE TABLE consulting_rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clinic_id UUID NOT NULL REFERENCES clinics(id) ON DELETE RESTRICT,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(120),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT consulting_rooms_code_not_blank CHECK (btrim(code) <> ''),
    CONSTRAINT consulting_rooms_clinic_code_unique UNIQUE (clinic_id, code),
    CONSTRAINT consulting_rooms_id_clinic_unique UNIQUE (id, clinic_id)
);

CREATE TABLE doctor_specialties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id UUID NOT NULL REFERENCES doctors(id) ON DELETE RESTRICT,
    specialty_id UUID NOT NULL REFERENCES specialties(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT doctor_specialties_unique UNIQUE (doctor_id, specialty_id)
);

CREATE TABLE doctor_clinics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id UUID NOT NULL REFERENCES doctors(id) ON DELETE RESTRICT,
    clinic_id UUID NOT NULL REFERENCES clinics(id) ON DELETE RESTRICT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT doctor_clinics_unique UNIQUE (doctor_id, clinic_id)
);

CREATE TABLE availability_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_clinic_id UUID NOT NULL REFERENCES doctor_clinics(id) ON DELETE CASCADE,
    weekday SMALLINT NOT NULL,
    starts_at TIME NOT NULL,
    ends_at TIME NOT NULL,
    slot_minutes SMALLINT NOT NULL,
    valid_from DATE,
    valid_until DATE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT availability_rules_weekday_valid CHECK (weekday BETWEEN 0 AND 6),
    CONSTRAINT availability_rules_period_valid CHECK (starts_at < ends_at),
    CONSTRAINT availability_rules_slot_valid CHECK (slot_minutes BETWEEN 5 AND 240),
    CONSTRAINT availability_rules_dates_valid CHECK (
        valid_until IS NULL OR valid_from IS NULL OR valid_from <= valid_until
    )
);

CREATE TABLE unavailabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_clinic_id UUID NOT NULL REFERENCES doctor_clinics(id) ON DELETE CASCADE,
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    reason VARCHAR(300),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT unavailabilities_period_valid CHECK (starts_at < ends_at)
);

CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE RESTRICT,
    doctor_id UUID NOT NULL REFERENCES doctors(id) ON DELETE RESTRICT,
    clinic_id UUID NOT NULL REFERENCES clinics(id) ON DELETE RESTRICT,
    consulting_room_id UUID,
    specialty_id UUID NOT NULL REFERENCES specialties(id) ON DELETE RESTRICT,
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    time_range TSTZRANGE GENERATED ALWAYS AS (
        tstzrange(starts_at, ends_at, '[)')
    ) STORED,
    status appointment_status NOT NULL DEFAULT 'confirmed',
    reason VARCHAR(500),
    cancellation_reason VARCHAR(500),
    cancelled_at TIMESTAMPTZ,
    cancelled_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    rescheduled_from_id UUID REFERENCES appointments(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT appointments_period_valid CHECK (starts_at < ends_at),
    CONSTRAINT appointments_room_matches_clinic FOREIGN KEY (consulting_room_id, clinic_id)
        REFERENCES consulting_rooms(id, clinic_id) ON DELETE RESTRICT,
    CONSTRAINT appointments_doctor_works_at_clinic FOREIGN KEY (doctor_id, clinic_id)
        REFERENCES doctor_clinics(doctor_id, clinic_id) ON DELETE RESTRICT,
    CONSTRAINT appointments_doctor_has_specialty FOREIGN KEY (doctor_id, specialty_id)
        REFERENCES doctor_specialties(doctor_id, specialty_id) ON DELETE RESTRICT,
    CONSTRAINT appointments_not_self_rescheduled CHECK (
        rescheduled_from_id IS NULL OR rescheduled_from_id <> id
    )
);

ALTER TABLE appointments
    ADD CONSTRAINT appointments_no_doctor_overlap
    EXCLUDE USING gist (
        doctor_id WITH =,
        time_range WITH &&
    ) WHERE (status IN ('pending', 'confirmed'));

ALTER TABLE appointments
    ADD CONSTRAINT appointments_no_patient_overlap
    EXCLUDE USING gist (
        patient_id WITH =,
        time_range WITH &&
    ) WHERE (status IN ('pending', 'confirmed'));

ALTER TABLE appointments
    ADD CONSTRAINT appointments_no_room_overlap
    EXCLUDE USING gist (
        consulting_room_id WITH =,
        time_range WITH &&
    ) WHERE (
        consulting_room_id IS NOT NULL
        AND status IN ('pending', 'confirmed')
    );

CREATE TABLE consultations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID NOT NULL UNIQUE REFERENCES appointments(id) ON DELETE RESTRICT,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ NOT NULL,
    clinical_summary TEXT,
    follow_up_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT consultations_period_valid CHECK (started_at < ended_at)
);

CREATE TABLE appointment_status_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID NOT NULL REFERENCES appointments(id) ON DELETE RESTRICT,
    old_status appointment_status,
    new_status appointment_status NOT NULL,
    changed_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    reason VARCHAR(500),
    changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX appointments_doctor_starts_at_idx
    ON appointments (doctor_id, starts_at);
CREATE INDEX appointments_patient_starts_at_idx
    ON appointments (patient_id, starts_at);
CREATE INDEX appointments_clinic_starts_at_idx
    ON appointments (clinic_id, starts_at);
CREATE INDEX appointment_status_history_appointment_changed_at_idx
    ON appointment_status_history (appointment_id, changed_at DESC);
CREATE INDEX availability_rules_doctor_clinic_weekday_idx
    ON availability_rules (doctor_clinic_id, weekday)
    WHERE is_active;
CREATE INDEX unavailabilities_doctor_clinic_starts_at_idx
    ON unavailabilities (doctor_clinic_id, starts_at);

CREATE OR REPLACE FUNCTION require_profile_role()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    account_role user_role;
BEGIN
    SELECT role
    INTO account_role
    FROM users
    WHERE id = NEW.user_id
    FOR KEY SHARE;

    IF account_role::TEXT <> TG_ARGV[0] THEN
        RAISE EXCEPTION 'User % must have the % role', NEW.user_id, TG_ARGV[0];
    END IF;

    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION prevent_profile_role_change()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.role = OLD.role THEN
        RETURN NEW;
    END IF;

    IF NEW.role <> 'patient' AND EXISTS (
        SELECT 1 FROM patients WHERE user_id = NEW.id
    ) THEN
        RAISE EXCEPTION 'A user with a patient profile must retain the patient role';
    END IF;

    IF NEW.role <> 'doctor' AND EXISTS (
        SELECT 1 FROM doctors WHERE user_id = NEW.id
    ) THEN
        RAISE EXCEPTION 'A user with a doctor profile must retain the doctor role';
    END IF;

    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION require_completed_appointment()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    current_status appointment_status;
BEGIN
    SELECT status
    INTO current_status
    FROM appointments
    WHERE id = NEW.appointment_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Appointment % does not exist', NEW.appointment_id;
    END IF;

    IF current_status <> 'completed' THEN
        RAISE EXCEPTION 'A consultation requires a completed appointment';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER users_set_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER users_prevent_profile_role_change
    BEFORE UPDATE OF role ON users
    FOR EACH ROW EXECUTE FUNCTION prevent_profile_role_change();
CREATE TRIGGER patients_require_patient_role
    BEFORE INSERT OR UPDATE OF user_id ON patients
    FOR EACH ROW EXECUTE FUNCTION require_profile_role('patient');
CREATE TRIGGER doctors_require_doctor_role
    BEFORE INSERT OR UPDATE OF user_id ON doctors
    FOR EACH ROW EXECUTE FUNCTION require_profile_role('doctor');
CREATE TRIGGER patients_set_updated_at
    BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER doctors_set_updated_at
    BEFORE UPDATE ON doctors
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER specialties_set_updated_at
    BEFORE UPDATE ON specialties
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER clinics_set_updated_at
    BEFORE UPDATE ON clinics
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER consulting_rooms_set_updated_at
    BEFORE UPDATE ON consulting_rooms
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER availability_rules_set_updated_at
    BEFORE UPDATE ON availability_rules
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER appointments_set_updated_at
    BEFORE UPDATE ON appointments
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER consultations_set_updated_at
    BEFORE UPDATE ON consultations
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER consultations_require_completed_appointment
    BEFORE INSERT OR UPDATE OF appointment_id ON consultations
    FOR EACH ROW EXECUTE FUNCTION require_completed_appointment();

COMMIT;
