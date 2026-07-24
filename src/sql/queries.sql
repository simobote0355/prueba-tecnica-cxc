SELECT 
    cod_apli_prod,
    descri_cod_apli_prod,
    num_cta,
    f_creacion,
    f_ultimo_pago,
    vlr_original,
    vlr_pagado,
    vlr_pendiente_pago,
    cod_trn,
    descri_cod_trn,
    ROUND(vlr_pagado / vlr_original, 4) AS porc_recuperado,
    CAST(
        julianday(
            substr(f_ultimo_pago, 1, 4) ||'-'||
            substr(f_ultimo_pago, 5, 2) ||'-'||
            substr(f_ultimo_pago, 7, 2)
        ) - 
        julianday(
            substr(f_creacion, 1, 4) ||'-'||
            substr(f_creacion, 5, 2) ||'-'||
            substr(f_creacion, 7, 2)
        ) AS INTEGER
    ) AS dias_hasta_ultimo_pago,
    CASE 
        WHEN vlr_pendiente_pago = 0 THEN 1 
        ELSE 0 
    END AS pago_total,
    CASE
        WHEN vlr_pagado = 0 THEN 1
        ELSE 0
    END AS sin_pago,
    CASE 
        WHEN vlr_pagado > 0 AND vlr_pendiente_pago > 0 THEN 1
        ELSE 0
    END AS pago_parcial
FROM tabla1;

