CREATE TABLE photos_metadata (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(150),
    make VARCHAR(60),
    -- FIXME: increased model from 30 to 50
    model VARCHAR(50),
    orientation_rotation VARCHAR(30),
    software VARCHAR(30),
    date_and_time VARCHAR(30),
    ycbcr_positioning VARCHAR(30),
    x_resolution VARCHAR(30),
    y_resolution VARCHAR(30),
    resolution_unit VARCHAR(25),
    exposure_time VARCHAR(15),
    f_number VARCHAR(10),
    exposure_program VARCHAR(30),
    exif_version VARCHAR(30),
    date_and_time_original VARCHAR(30),
    date_and_time_digitized VARCHAR(30),
    components_configuration VARCHAR(25),
    exposure_bias VARCHAR(30),
    -- FIXME: changed metering_mode from 20 to 50
    metering_mode VARCHAR(50),
    -- FIXME: changed flash from 40 to 100
    flash VARCHAR(100),
    focal_length VARCHAR(10),
    maker_note VARCHAR(100),
    flashpix_version VARCHAR(35),
    -- FIXME: changed color_space from 20 to 50
    color_space VARCHAR(50),
    interoperability_index VARCHAR(10),
    -- FIXME: changed interoperability from 20 to 50
    interoperability_version VARCHAR(20));


-- Aight, look. We type coerced everything into only strings because it's difficult trying to convert
-- Idftag (?) types into float/num for columns that needed those types. Somehow, just converting them
-- from Idftag to string made the column data work, so we're sticking with that. And that's final.
-- Sorry.

-- If you know how to convert Idftag to float/num successfully, please let us know.


