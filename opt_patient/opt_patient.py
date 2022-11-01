# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit='res.partner'
    m2o_child_id = fields.Many2one('opt.patient', string='Addresses')

class OptPatient(models.Model):
    _name = 'opt.patient'
    # _inherit='spec.referred.by'
    _description='Hospital Patient'

    name = fields.Char('First Name', store=True,required=True)

    title= fields.Selection(
        [
            ('mr','Mr'),
            ('mrs','Mrs'),
            ('ms','Ms'),
            ('miss','Miss'),
            ('mix','Mx'),
        ],
        default = "mr"
    )
    

    # first_name = fields.Char()
    middle_name = fields.Char()
    middle_name = fields.Char()
    last_name = fields.Char()
    suffix = fields.Char()
    
    image_1920 = fields.Binary()


    # Profile 
    # For Left Hand file 

    nick_name = fields.Char(string="Nickname")




    phone = fields.Char('Cell')
    update_label_cell = fields.Boolean("Update")




    other = fields.Char('Other')

    email = fields.Char('Email')

    ## For Address 
    street = fields.Char('Address')
    street2 = fields.Char('Address')
    city = fields.Char("City")
    state_id = fields.Many2one('res.country.state')
    zip = fields.Char("ZIP")
    country_id = fields.Many2one("res.country")
    ## End of Address

    referred_by_id =  fields.Many2one('spec.referred.by')

    date_of_birth = fields.Date(string="Date of Birth")

    ssn = fields.Char(string="SSN")
    
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('unspecified', 'Unspecified')
        ],
        default = "unspecified"
    )

    gender_identification = fields.Selection(
        [
            ('indentifies_as_male', 'Indentifies as Male'),
            ('indentifies_as_female', 'Indentifies as Female'),
            ('ftm_transgender_male', 'Female-to-Male (FTM)/Transgender Male'),
            ('mtf_transgender_female', 'Male-to-Female (MTF)/ Transgender Female'),
            ('indentifies_confirming_gender', 'Identifies as non-confirming gender'),
            ('additional_gender_category_other', 'Additional gender category or other'),
            ('choose_not_disclose', 'Choose not to disclose')
        ]
    )

    marital_status = fields.Selection(
        [
            ('single', 'Single'),
            ('married', 'Married'),
            ('Divorced', 'Divorced'),
            ('widowed', 'Widowed')
        ],
    )

    occupation = fields.Char(string="Occupation")


    # Profile 
    # For Right Hand file 

    preferred_language = fields.Selection(
        [
            ('declined_to_Specify','Declined to Specify'),
            ('unspecified','Unspecified'),
            ('english','English'),
            ('spanish','Spanish'),
            ('french','French'),
            ('german','German'),
        ]
    )

    race = fields.Selection(
        [
            ('declined','Declined'),
            ('american_indian','American Indian'),
            ('asian','Asian'),
            ('native_pacific_islander','Native Hawaiian or Other Pacific Islander'),
            ('black_or_african_american','Black or African American'),
            ('white','White'),
            ('other','Other'),
        ]
    )

    ethnicity = fields.Selection(
        [
            ('declined_to_Specify','Declined to Specify'),
            ('american_indian_Alaska_native','American Indian or Alaska Native'),
            ('asian','Asian'),
            ('black_or_african_american','Black or African American'),
            ('native_spacific_islander','Native Hawaiian or Other Pacific Islander'),
            ('white','White'),
        ]
    )

    

    partner_id = fields.Many2one('res.partner')

    hipaa_sign = fields.Boolean(string="Signature on file")

    provide = fields.Many2one('hr.employee')

    company_id = fields.Many2one('res.company')

    active = fields.Boolean(string="Active", default=True)

    deceased = fields.Boolean(string="Deceased")

    emergency_name = fields.Char(string="Emergency Contact")

    emergency_phone = fields.Char(string="Emergency Phone")

    communication_preferences = fields.Selection(
        [
            ('email','Email'),
            ('phone','Phone'),
            ('cell','Cell')
        ]
    )

    select_all = fields.Boolean(string="Select All")


    communication_ids = fields.One2many(comodel_name = 'spec.communication.table', inverse_name='m2o_communication_id')  

    contact_lens_ids = fields.One2many(comodel_name = "spec.contact.lenses", inverse_name='m2o_spec_contact_lenses')
    
    insurance_ids = fields.One2many(comodel_name = 'spec.insurance', inverse_name='m2o_spec_insurance')

    documents_ids = fields.One2many(comodel_name = 'multi.images', inverse_name='m2o_multi_images')

    recall_type_ids = fields.One2many(comodel_name = 'spec.recall.type.line', inverse_name='recall')


    family_ids = fields.Many2many(comodel_name = 'res.partner')  

    insurance_authorizations_ids = fields.One2many(comodel_name='spec.insurance.authorizations', inverse_name='m2o_insurance_authorization_id')

    child_ids = fields.One2many(comodel_name='res.partner', inverse_name='m2o_child_id')
    
    
    @api.onchange('select_all')
    def _onchange_select_all(self):
        for communication_id in self.communication_ids:
            if self.select_all:
                communication_id.text = True
                communication_id.cell = True
                communication_id.email = True
                communication_id.mail = True
                communication_id.opt_out = False
            else:
                communication_id.text = False
                communication_id.cell = False
                communication_id.email = False
                communication_id.mail = False
    
    @api.model
    def default_get(self, fields):
        defaults = super(OptPatient, self).default_get(fields)
        if not self._context.get('is_user'):
            country_id = self.env.ref('base.us')
            defaults['country_id'] = country_id.id
            defaults['select_all'] = True
            communication_list = ['Appointment', 'Recall', 'Order Pick-up', 'General']
            dic_list = []
            for communication in communication_list:
                dic_list.append((0, 0, {'communication': communication}))
        defaults['communication_ids'] = dic_list
        return defaults





    def appointments_list_view(self):
        self.ensure_one()
        _list = self.env.ref('opt_appointment.calendar_event_from_patient_form', False)
        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'view_type': 'list',
            'view_mode': 'list',
            'target': 'current',
            # 'view_id': [(_list and _list.id)],
            # 'views': [(_list and _list.id, 'list')],
            # 'domain': [('patient_id', '=', self.id), ('appointment_type', '=', 'appointment')],
        }



    def action_view_partner_invoices(self):
        self.ensure_one()
        # action = {
        #     'name': _('Invoices'),
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'account.move',
        #     'view_type': 'tree,kanban,form',
        #     'view_mode': 'tree,kanban,form',
        #     'target': 'current',
        #     'views': [(self.env.ref('account.view_invoice_tree').id, 'list'),
        #               (False, 'form'), (False, 'kanban')],
        #     'domain': [
        #         ('type', 'in', ('out_invoice', 'out_refund')),
        #         ('partner_id', '=', self.id),
        #     ],
        #     'context': {
        #         'default_type': 'out_invoice',
        #         'type': 'out_invoice',
        #         'journal_type': 'sale',
        #         # 'search_default_unpaid': 1
        #     }
        # }
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]


        ####
        ####
        # These Lines are commented by me 
        ####
        ####


        # action['domain'] = [
        #     ('type', 'in', ('out_invoice', 'out_refund')),
        #     ('partner_id', 'child_of', self.id),
        # ]
        # action['context'] = {
        #     'default_type': 'out_invoice',
        #     'type': 'out_invoice',
        #     'journal_type': 'sale',
        # }
        return action

    def open_consent_form(self):
        tree = self.env.ref('acs_consent_form.view_acs_consent_form_tree_in_patient', False)
        return {
            'name': "Consent Forms",
            'type': 'ir.actions.act_window',
            'res_model': 'acs.consent.form',
            'view_mode': 'form',
            'target': 'current',
            'domain': [('partner_id', '=', self.id)],
            'views': [(tree and tree.id, 'tree'),(None, 'form')],
            # 'context': {'default_partner_id': self.id,
            #             'default_user_id': self.user_ids[0].id if len(self.user_ids) else None}
        }


    def sales_list_view(self):
        self.ensure_one()
        return {
            'name': 'Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_type': 'list,form',
            'view_mode': 'list,form',
            'target': 'current',
            'views': [(False, 'list'), (False, 'form')],
            'domain': [('partner_id', '=', self.id)],
        }
    
    def open_credit_notes(self):
        self.ensure_one()
        # action = self.env.ref('account.action_move_out_refund_type').read()[0]
        # action['name'] = 'Credit Notes'
        # action['domain'] = [('partner_id', '=', self.id), ('type', '=', 'out_refund')]
        # return action
        return {
            'name': 'Credit Notes',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_type': 'list,form',
            'view_mode': 'list,form',
            'target': 'current',
            # 'views': [('account.view_invoice_tree', 'list'), (False, 'form')],
            # 'domain': [('partner_id', '=', self.id), ('type', '=', 'out_refund')],
        }



    # Adding record in res.partner 
    # @ api.model
    # def create(self, vals):

    #     print("\n\n Called \n\n")

    #     res = super(OptPatient, self).create(vals)
    #     self.env['res.partner'].create(
    #         {
    #             'name':self.first_name,
    #             'image_1920': self.image_1920,
    #             'phone': self.phone,
    #             'email':self.email,
    #         }
    #     )
    #     return res





class SpecInsurance(models.Model):
    _name = 'my.spec.insurance'
    _description = 'This is my own spec.insurance'

    name_with_termination_date = fields.Char(string="Insurance", readonly=True)

    sequence = fields.Char(string="Insurance ID")

    termination_date = fields.Date(
        string='Termination',
        default=fields.Date.context_today,
    )
    
    priority = fields.Selection(
        [
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('tertiary', 'Tertiary'),
        ]
    )

    insurance_type = fields.Selection(
        [
            ('medical', 'Medical'),
            ('vision', 'Vision'),
        ]
    )

    m2o_spec_insurance= fields.Many2one("opt.patient", string='Insurance') 


    

class SpecContactLensesInherit(models.Model):
    _inherit = 'spec.contact.lenses'
    m2o_spec_contact_lenses = fields.Many2one("opt.patient", string='Rx') 

class MultiImagesInherit(models.Model):
    _inherit = 'multi.images'
    m2o_multi_images= fields.Many2one("opt.patient", string='Documents') 

class SpecRecallTypeLineInherit(models.Model):
    _inherit = 'spec.recall.type.line'
    recall = fields.Many2one('opt.patient')

class SpecCommunicationTableInherit(models.Model):
    _inherit = 'spec.communication.table'
    m2o_communication_id = fields.Many2one('opt.patient', string='Communication Table')





