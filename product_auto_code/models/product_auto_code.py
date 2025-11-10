from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import random


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.constrains('default_code')
    def _check_unique_default_code(self):
        """
        Verifica que el código interno sea único entre todas las variantes.
        """
        for record in self:
            if record.default_code:
                duplicate = self.search([
                    ('default_code', '=', record.default_code),
                    ('id', '!=', record.id)
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        _("El código de referencia '%s' ya existe. Debe ser único.") % record.default_code
                    )

    @api.model
    def create(self, vals_list):
        """
        Crea productos y genera un código automático si no se define.
        Si se define un código repetido, lanza error y evita importar/crear.
        """
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        new_records = self.browse()

        for vals in vals_list:
            default_code = vals.get('default_code')

            # Si tiene código definido → verificar que no exista
            if default_code:
                if self.search([('default_code', '=', default_code)], limit=1):
                    raise ValidationError(
                        _("El código de referencia '%s' ya existe. Debe ser único.") % default_code
                    )
            else:
                # Si no tiene código → generar uno automáticamente
                vals['default_code'] = self._generate_unique_code()

            record = super(ProductProduct, self).create(vals)
            new_records += record

        return new_records

    def _generate_unique_code(self):
        """
        Genera un número aleatorio de 6 dígitos que no esté repetido.
        """
        while True:
            code = f"{random.randint(0, 999999):06d}"
            if not self.search([('default_code', '=', code)], limit=1):
                return code


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        """
        Si el producto padre no tiene código, lo toma de su primera variante.
        """
        template = super().create(vals)

        if not template.default_code and template.product_variant_id:
            template.default_code = template.product_variant_id.default_code

        return template

    def _create_variant_ids(self):
        """
        Al agregar nuevas variantes a un producto existente,
        se asegura de que cada una tenga un código único.
        """
        res = super()._create_variant_ids()

        for template in self:
            for variant in template.product_variant_ids:
                if not variant.default_code:
                    variant.default_code = variant._generate_unique_code()

        return res
