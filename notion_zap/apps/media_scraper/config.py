from notion_zap.cli.structs import (
    PropertyColumn as Cl, PropertyMarkedValue as Lb, PropertyFrame)

_STATUS_MARKS = [
    Lb('π₯λ³Έλ¬Έ/μμΉ(λΉνκ΄΄)', 'default',
       ('queue', 'manually_confirm', 'metadata', 'location',)),
    Lb('π₯λ³Έλ¬Έ(νκ΄΄)', 'metadata', ('queue', 'completely', 'metadata', 'overwrite', )),
    Lb('π₯μμΉ(νκ΄΄)', 'location', ('queue', 'manually_confirm', 'location', 'overwrite', )),
    Lb('β³μν© μλ£', 'completely', ('success', )),
    Lb('β­μ λ³΄ μμ', 'pass', ('success', )),
    Lb('π€μ§μ  μλ ₯', 'fill_manually', ('success', )),
    Lb('π€κ²°κ³Ό κ²μ ', 'manually_confirm', ('success', )),
    Lb('βλ§ν¬ μμ', 'no_meta_url', ('fail', )),
    Lb('βμμΉ μμ', 'no_location', ('fail', )),
]
STATUS_COLUMN = Cl(key='πμ€λΉ', alias='edit_status',
                   marked_values=_STATUS_MARKS)

READING_FRAME = PropertyFrame([
    Cl(key='πμ ν', alias='media_type', ),
    Cl(key='πλμλ₯', alias='is_book'),
    STATUS_COLUMN,
    Cl(key='πμ λͺ©', aliases=['docx_name', 'title']),
    Cl(key='πμμ (κ²μμ©)', alias='true_name'),
    Cl(key='πλΆμ ', alias='subname'),
    Cl(key='πλ§ν¬', alias='url'),
    Cl(key='πλ§λ μ΄', alias='author'),
    Cl(key='πλ§λ κ³³', alias='publisher'),
    Cl(key='πN(μͺ½)', alias='volume'),
    Cl(key='πνμ§', alias='cover_image'),
    Cl(key='πμμΉ', alias='location'),
    Cl(key='πλμΆμ€', alias='not_available'),
    Cl(key='π¦κ²°μ', alias='link_to_contents'),
])
