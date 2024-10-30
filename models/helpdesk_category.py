from odoo import models,fields, api


class HelpDeskCategory(models.Model):
    _name = 'helpdesk.category'
    _description = 'Help Desk Category'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Category Name", required=True,tracking=True)
    team_id = fields.Many2one('helpdesk.team', string="Team", required=True)
    description = fields.Text(string="Description")

    ticket_count = fields.Integer(string="Total Tickets", compute='_compute_ticket_counts', store=True)
    solved_ticket_count = fields.Integer(string="Solved Tickets", compute='_compute_ticket_counts', store=True)

    total_ticket_count = fields.Integer(string="Total Tickets Across All Categories",
                                        compute='_compute_total_ticket_counts', store=False)
    total_solved_ticket_count = fields.Integer(string="Total Solved Tickets Across All Categories",
                                               compute='_compute_total_ticket_counts', store=False)

    @api.depends('name')
    def _compute_ticket_counts(self):
        for category in self:
            tickets = self.env['helpdesk.ticket'].search([('category_id', '=', category.id)])
            category.ticket_count = len(tickets)
            category.solved_ticket_count = len(tickets.filtered(lambda t: t.state == 'done'))

    @api.depends('ticket_count', 'solved_ticket_count')
    def _compute_total_ticket_counts(self):
        total_tickets = self.env['helpdesk.ticket'].search([])
        total_solved_tickets = total_tickets.filtered(lambda t: t.state == 'done')

        # Set the total counts for all categories
        self.total_ticket_count = len(total_tickets)
        self.total_solved_ticket_count = len(total_solved_tickets)

    def action_ticket(self):
        return {
            'name': 'Tickets',
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket',
            'view_mode': 'kanban,tree,form',
            'domain': [('category_id', '=', self.id)],  # Filter by current category
        }

