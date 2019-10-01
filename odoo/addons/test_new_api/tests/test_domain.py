# -*- coding: utf-8 -*-
from odoo.tests import common, Form


class test_domain(common.TransactionCase):

    def setUp(self):
        super(test_domain, self).setUp()
        self.bool = self.env['domain.bool']

    def test_00_test_bool_undefined(self):
        """
        Check that undefined/empty values in database is equal to False and different of True

        """

        # Add a new boolean column after that some rows/tuples has been added (with data)
        # Existing rows/tuples will be undefined/empty
        self.env['ir.model.fields'].create({
            'name': 'x_bool_new_undefined',
            'model_id': self.env.ref('test_new_api.model_domain_bool').id,
            'field_description': 'A new boolean column',
            'ttype': 'boolean'
        })

        self.env.ref('test_new_api.bool_3').write({'x_bool_new_undefined': True})
        self.env.ref('test_new_api.bool_4').write({'x_bool_new_undefined': False})

        model = self.bool
        all_bool = model.search([])
        for f in ['bool_true', 'bool_false', 'bool_undefined', 'x_bool_new_undefined']:
            eq_1 = model.search([(f, '=', False)])
            neq_1 = model.search([(f, '!=', True)])
            self.assertEqual(eq_1, neq_1, '`= False` (%s) <> `!= True` (%s) ' % (len(eq_1), len(neq_1)))

            eq_2 = model.search([(f, '=', True)])
            neq_2 = model.search([(f, '!=', False)])
            self.assertEqual(eq_2, neq_2, '`= True` (%s) <> `!= False` (%s) ' % (len(eq_2), len(neq_2)))

            self.assertEqual(eq_1+eq_2, all_bool, 'True + False != all')
            self.assertEqual(neq_1+neq_2, all_bool, 'not True + not False != all')

    def test_form_domain(self):
        """
        Check domain attribute works as expected
        """

        bar1 = self.env['test_new_api.bar'].create({
            'name': '1',
            'is_good': True,
        })
        baz = Form(self.env['test_new_api.baz'])
        baz.is_good = True
        baz.bar = bar1
        assert baz.bar == bar1
        assert baz.bar.is_good is True
        baz.bar = self.env['test_new_api.bar'].create({
            'name': '2',
            'is_good': False,
        })
        assert baz.bar.is_good is False  # wrong, domain was avoided!!!
        baz = baz.save()
        assert baz
        assert baz.is_good != baz.bar.is_good  # T_T
