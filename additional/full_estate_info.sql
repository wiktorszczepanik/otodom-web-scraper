/* 
sample of integration collected inforations about estates with filters:
- mieszkania (apartments)
- wynajem (rent)
*/

-- first lvl - information about particular estate (page and base)
CREATE TABLE IF NOT EXISTS page_base AS 
SELECT * FROM page_info
INNER JOIN base_info ON
page_info.ROWID = base_info.ROWID;

-- 2nd lvl - information about particular estate (specific and additional)
CREATE TABLE IF NOT EXISTS spec_addit AS 
SELECT * FROM specific_info_miewyn
INNER JOIN additional_info_miewyn ON
specific_info_miewyn.ROWID = additional_info_miewyn.ROWID;

-- create full info about estates
-- 1. replece first '*' to columns that you need
-- 2. replece uuid with yours
CREATE TABLE IF NOT EXISTS full_estate_info AS 
SELECT * -- here 1.
FROM (SELECT * FROM page_base
INNER JOIN spec_addit ON
page_base.ROWID = spec_addit.ROWID)
WHERE uuid LIKE '0687f25c-cea4-406e-8f22-daa262ba40ab' -- here 2.
ORDER BY id;

-- access full info
SELECT *
FROM full_estate_info;