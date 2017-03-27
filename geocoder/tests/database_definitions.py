"""
Definicion de las funciones que forman el geocodificador en la base de datos.
Usarlas para cargarlas en la base de los tests.
"""


existe_calle = '''
CREATE OR REPLACE FUNCTION existe_calle(calle text)
RETURNS BOOL AS $$
DECLARE
  resultado BOOL;
BEGIN
  SELECT lower(calle) IN (SELECT DISTINCT nombre FROM calles_geocod) INTO resultado;

  RETURN resultado;
END;
$$ LANGUAGE 'plpgsql';
'''

altura_total_calle = '''
CREATE OR REPLACE FUNCTION altura_total_calle(calle text)
RETURNS int4range AS $$
DECLARE
  resultado int4range;
BEGIN
  SELECT int4range(min(alt_i), max(alt_f))
  FROM calles_geocod
  WHERE (alt_i != 0 AND alt_f != 1 AND alt_i < alt_f) AND nombre = calle
  GROUP BY nombre
  INTO resultado;

  RETURN resultado;
END;
$$ LANGUAGE 'plpgsql';
'''

existe_altura = '''
CREATE OR REPLACE FUNCTION existe_altura(calle text, altura integer)
RETURNS BOOL AS $$
DECLARE
  resultado BOOL;
BEGIN
  SELECT (SELECT altura_total_calle(calle)) @> altura
  INTO resultado;

  RETURN resultado;
END;
$$ LANGUAGE 'plpgsql';
'''

union_geom = '''
CREATE OR REPLACE FUNCTION union_geom(calle text)
  RETURNS geometry AS $$
DECLARE resultado geometry;
BEGIN
  SELECT st_union(array_agg(c.geom))
  FROM calles_geocod c
  WHERE nombre = lower(calle)
  INTO resultado;

  RETURN resultado;
END;
$$ LANGUAGE 'plpgsql';
'''

# union_geom version 2
union_geom_v2 = '''
CREATE OR REPLACE FUNCTION union_geom(calle text, altura_i integer, altura_f integer)
  RETURNS geometry AS $$
DECLARE resultado geometry;
BEGIN

  SELECT st_union(array_agg(c.geom))
  FROM calles_geocod c
  WHERE nombre = lower(calle)
  AND
  (alt_i != 0 AND alt_f != 1 AND alt_i < alt_f)
  AND
  (alt_i >= altura_i AND alt_f <= altura_f)
  INTO resultado;

  RETURN st_transform(resultado, 3857);
END;
$$ LANGUAGE 'plpgsql';
'''

punto_interseccion = '''
CREATE OR REPLACE FUNCTION punto_interseccion(calle1 text, calle2 text)
  RETURNS GEOMETRY AS $$
DECLARE resultado GEOMETRY;
BEGIN
  IF (st_crosses(union_geom(calle1), union_geom(calle2))) OR
     (st_touches(union_geom(calle1), union_geom(calle2)))
     THEN
     SELECT ST_Intersection(union_geom(calle1), union_geom(calle2)) limit 1
     INTO resultado;

     IF st_numgeometries(resultado) > 1
     THEN
     resultado := st_geometryn(resultado, 1);
     END IF;

  ELSE
    resultado := NULL;
  END IF;

  RETURN resultado;
END;
$$ LANGUAGE 'plpgsql';
'''

altura_direccion_calle = '''
CREATE OR REPLACE FUNCTION altura_direccion_calle(calle text, altura integer)
  RETURNS GEOMETRY AS
$$
DECLARE resultado GEOMETRY;
BEGIN

  SELECT ST_LineInterpolatePoint(ST_LineMerge((SELECT geom
  FROM calles_geocod
  WHERE rango @> altura
  AND nombre = lower(calle) LIMIT 1)), (altura % 100)::float / 100)
  INTO resultado;

  RETURN resultado;

END;
$$ LANGUAGE 'plpgsql';
'''

cabildo_2000 = {'id': 2207,
                'codigo': 3005,
                'nombre': 'cabildo',
                'alt_i': 2000,
                'alt_f': 2100,
                'tipo': 'avenida',
                'geom': '0105000020E610000001000000010200000002000000B07D48065A3A4DC0C0969D05104841C0B0212EED743A4DC05091ADC8F04741C0',
                'rango': '[2000,2100)',
                'geom_3857': '0105000020110F000001000000010200000002000000B8EE457CC3D258C112C71D45E5504FC130265155DAD258C1C67C4ED6A4504FC1',}

cabildo_2100 = {'id': 2097,
                'codigo': 3005,
                'nombre': 'cabildo',
                'alt_i': 2100,
                'alt_f': 2200,
                'tipo': 'avenida',
                'geom': '0105000020E610000001000000010200000003000000B0212EED743A4DC05091ADC8F04741C090067BF5823A4DC0B0B4667DE04741C03821CB958F3A4DC0D0EF81A4D14741C0',
                'rango': '[2100,2200)',
                'geom_3857': '0105000020110F00000100000001020000000300000030265155DAD258C1C67C4ED6A4504FC105424240E6D258C19D30893A83504FC1769376F9F0D258C1CC51C59A64504FC1',}

juramento_2350 = {'id': 2096,
                 'codigo': 10017,
                 'nombre': 'juramento',
                 'alt_i': 2350,
                 'alt_f': 2400,
                 'tipo': 'avenida',
                 'geom': '0105000020E610000001000000010200000002000000188EF4D0613A4DC0A05EF40BE74741C0B0212EED743A4DC05091ADC8F04741C0',
                 'rango': '[2350,2400)',
                 'geom_3857': '0105000020110F0000010000000102000000020000005D4D591ACAD258C1DC8FC0C090504FC130265155DAD258C1C67C4ED6A4504FC1',}

juramento_2400 = {'id': 2163,
                 'codigo': 10017,
                 'nombre': 'juramento',
                 'alt_i': 2400,
                 'alt_f': 2500,
                 'tipo': 'avenida',
                 'geom': '0105000020E610000001000000010200000002000000B0212EED743A4DC05091ADC8F04741C010C6AE11953A4DC0C0E6CCC1034841C0',
                 'rango': '[2400,2500)',
                 'geom_3857': '0105000020110F00000100000001020000000200000030265155DAD258C1C67C4ED6A4504FC1CA68C9A1F5D258C14F6AC8F8CB504FC1',}
