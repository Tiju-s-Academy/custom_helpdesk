from odoo import models,fields


class HelpDeskCategory(models.Model):
    _name = 'helpdesk.category'
    _description = 'Help Desk Category'

    name = fields.Char(string="Category Name", required=True)
    team_id = fields.Many2one('helpdesk.team', string="Team", required=True)
    description = fields.Text(string="Description")
