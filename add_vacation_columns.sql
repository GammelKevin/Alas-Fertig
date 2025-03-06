ALTER TABLE opening_hours ADD COLUMN vacation_start DATE;
ALTER TABLE opening_hours ADD COLUMN vacation_end DATE;
ALTER TABLE opening_hours ADD COLUMN vacation_active BOOLEAN DEFAULT FALSE;
