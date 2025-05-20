odoo.define('project_management.tooltip_safe', function (require) {
    'use strict';
    const $ = require('jquery');
    if (!$.fn.tooltip) {
        $.fn.tooltip = function () {
            return this;
        };
    }
});