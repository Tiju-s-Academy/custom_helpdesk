from odoo import models,fields


class HelpDeskTeam(models.Model):
    _name = 'helpdesk.team'
    _description = 'Help Desk Team'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Team Name", required=True)
    member_ids = fields.Many2many('res.users', string="Team Members")
