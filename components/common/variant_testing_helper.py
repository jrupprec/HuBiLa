
from itertools import product
from jinja2 import Template
import yaml


_jinja_template_string = """You are {{name}}. 
\n Facts about yourself: {{socio_behavioral}}. 
\n Facts about the apartment: {{apartment}}. 
\n Your goal: {{target}}. 
\n Never forget the following rules: 
- Do not tell the other party the facts stated above. 
- Only talk about the rental price. Do not talk about additional responsibilities, lease term conditions, or utility costs like heating, water, or electricity.
- If you want to accept the rental price proposed by the other party respond with the following sentence, where x is the final price that you want to agree with: 'I agree to the price of [x] Euro!' 
- If you don't want to continue the negotiation respond with the following sentence with a reason why you don't want to continue: 'I don't want to continue the negotiation, because [reason].'
- If you and the other party agreed on a price, the negotiation will be terminated. Respond with the following sentence: 'TERMINATE'
- If you and the other party did not agree on a price, the negotiation will be terminated. Respond with the following sentence: 'TERMINATE'"""


def _load_yaml_data(subfolder: str, yaml_content: str):
    with open(
        f"assets/prompts/{subfolder}/{yaml_content}.yaml", "r", encoding="utf-8"
    ) as file:
        return yaml.safe_load(file)


def _load_landlord_config():
    return (
        _load_yaml_data("landlord", yaml_content)
        for yaml_content in [
            "name",
            "socio-behavioral",
            "target",
        ]
    )


def _load_renter_config():
    return (
        _load_yaml_data("renter", yaml_content)
        for yaml_content in ["name", "socio-behavioral", "target"]
    )


def _load_product_config():
    for item in _load_yaml_data("product", "apartment"):
        yield item


def all_landlord_variants():
    name, socio_behavioral, target = _load_landlord_config()
    apartment = _load_product_config()

    variants = product(name, socio_behavioral, target, apartment)

    return [
        (
            {
                "name_id": name["id"],
                "socio_behavioral_id": socio_behavioral["id"],
                "target_id": target["id"],
                "apartment_id": apartment["id"],
            },
            render_system_message(
                name["content"],
                socio_behavioral["content"],
                target["content"],
                apartment["content"],
            ),
        )
        for name, socio_behavioral, target, apartment in variants
    ]


def all_renter_variants():
    name, socio_behavioral, target = _load_renter_config()
    apartment = _load_product_config()

    variants = product(name, socio_behavioral, target, apartment)

    return [
        (
            {
                "name_id": name["id"],
                "socio_behavioral_id": socio_behavioral["id"],
                "target_id": target["id"],
                "apartment_id": apartment["id"],
            },
            render_system_message(
                name["content"],
                socio_behavioral["content"],
                target["content"],
                apartment["content"],
            ),
        )
        for name, socio_behavioral, target, apartment in variants
    ]


def all_variants():
    landlord_variants = all_landlord_variants()
    renter_variants = all_renter_variants()

    all_variants = product(landlord_variants, renter_variants)

    return [(variant) for variant in all_variants]


def single_factor_variants_apartment():
    apartment = _load_product_config()
    # landlord_renter = landlord_renter_combination()

    landlord_name, landlord_socio_behavioral, landlord_target = _load_landlord_config()
    renter_name, renter_socio_behavioral, renter_target = _load_renter_config()

    landlord_renter = [
        (
            {
                "name_id": landlord_name[0]["id"],
                "socio_behavioral_id": landlord_socio_behavioral[0]["id"],
                "target_id": landlord_target[0]["id"],
            },
            {
                "name_id": renter_name[0]["id"],
                "socio_behavioral_id": renter_socio_behavioral[0]["id"],
                "target_id": renter_target[0]["id"],
            },
        )
    ]

    factor_variants = product(landlord_renter, apartment)

    return [
        (
            variant,
            {
                "landlord_system_message": render_system_message(
                    landlord_name[0]["content"],
                    landlord_socio_behavioral[0]["content"],
                    landlord_target[0]["content"],
                    variant[1]["content"],
                ),
                "renter_system_message": render_system_message(
                    renter_name[0]["content"],
                    renter_socio_behavioral[0]["content"],
                    renter_target[0]["content"],
                    variant[1]["content"],
                ),
            },
        )
        for variant in factor_variants
    ]


def single_factor_variants_renter_name():
    apartment = list(_load_product_config())
    landlord_name, landlord_socio_behavioral, landlord_target = _load_landlord_config()
    renter_name, renter_socio_behavioral, renter_target = _load_renter_config()

    renter = [
        (
            {
                "name_id": name["id"],
                "socio_behavioral_id": renter_socio_behavioral[0]["id"],
                "target_id": renter_target[0]["id"],
                "apartment_id": apartment[0]["id"],
                "renter_system_message": render_system_message(
                    name["content"],
                    renter_socio_behavioral[0]["content"],
                    renter_target[0]["content"],
                    apartment[0]["content"],
                ),
            }
        )
        for name in renter_name
    ]

    landlord = [
        (
            {
                "name_id": name["id"],
                "socio_behavioral_id": landlord_socio_behavioral[0]["id"],
                "target_id": landlord_target[0]["id"],
                "apartment_id": apartment[0]["id"],
                "landlord_system_message": render_system_message(
                    name["content"],
                    landlord_socio_behavioral[0]["content"],
                    landlord_target[0]["content"],
                    apartment[0]["content"],
                ),
            }
        )
        for name in landlord_name
    ]

    factor_variants = product(landlord, renter)
    factor_variants = list(factor_variants)

    variants = [[variant] for variant in factor_variants]

    return variants


def render_system_message(
    name: str, socio_behavioral: str, target: str, apartment: str
) -> str:
    jinja_template = Template(_jinja_template_string)

    return jinja_template.render(
        name=name,
        socio_behavioral=socio_behavioral,
        target=target,
        apartment=apartment,
    )


# example all variants
output = single_factor_variants_renter_name()
print(output[4])
# print(output)
# all = single_factor_variants_renter_name()
# print(len(all))
# print(all)
# print(all[0][0])
# print(all[0][0][1])
# print(output[0][1]["renter_system_message"])
# for variant in output:
#     print(f"Variant:" + str(variant[0][0]["landlord_system_message"]))
