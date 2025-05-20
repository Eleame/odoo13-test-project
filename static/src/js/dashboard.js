odoo.define('project_management.dashboard', function(require){
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var MyDashboard = AbstractAction.extend({
        start: function() {
            this.$el.html('<h1>Dashboard</h1>');
            return this._super.apply(this, arguments);
        }
    });

    core.action_registry.add('project_management.dashboard', MyDashboard);

    return MyDashboard;
});
