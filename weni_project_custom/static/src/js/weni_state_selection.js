odoo.define("weni_project_custom.weni_state", function (require) {
    "use strict";

    var StateSelectionWidget = require("web.basic_fields").StateSelectionWidget;
    var fieldRegistry = require("web.field_registry");
    var core = require("web.core");
    var rpc = require("web.rpc");

    var qweb = core.qweb;

    var WeniStateSelection = StateSelectionWidget.extend({
        _prepareDropdownValues: async function () {
            var self = this;
            var _data = [];
            var promises = [];
            var current_stage_id =
                self.recordData.stage_id && self.recordData.stage_id[0];
            var stage_data = {
                id: current_stage_id,
                legend_normal: this.recordData.legend_normal || undefined,
                legend_blocked: this.recordData.legend_blocked || undefined,
                legend_done: this.recordData.legend_done || undefined,
            };
            _.map(this.field.selection || [], async function (selection_item) {
                var value = {
                    name: selection_item[0],
                    tooltip: selection_item[1],
                };
                if (selection_item[0] === "normal") {
                    value.state_name = stage_data.legend_normal
                        ? stage_data.legend_normal
                        : selection_item[1];
                } else if (selection_item[0] === "done") {
                    value.state_class = "o_status_green";
                    value.state_name = stage_data.legend_done
                        ? stage_data.legend_done
                        : selection_item[1];
                } else {
                    var promise = rpc
                        .query({
                            model: "project.task.kanban.state",
                            method: "search_records_by_name",
                            args: [selection_item[0]],
                        })
                        .then(function (results) {
                            if (results.length > 0) {
                                results.forEach(function (stateItem) {
                                    if (selection_item[0] === stateItem.name) {
                                        value.state_name = stateItem.name;
                                        value.state_style = stateItem.color;
                                    }
                                });
                            } else {
                                value.state_class = "o_status_red";
                                value.state_name = stage_data.legend_blocked
                                    ? stage_data.legend_blocked
                                    : selection_item[1];
                            }
                        });
                    promises.push(promise);
                }
                _data.push(value);
            });
            await Promise.all(promises);
            return _data;
        },

        _render: async function () {
            var states = await this._prepareDropdownValues();
            var currentState = _.findWhere(states, {name: this.value}) || states[0];
            this.$(".o_status")
                .removeClass("o_status_red o_status_green o_status_blue")
                .css("background-color", currentState.state_style || "")
                .addClass(currentState.state_style ? "" : currentState.state_class)
                .prop("special_click", true)
                .parent()
                .attr("title", currentState.state_name)
                .attr("aria-label", this.string + ": " + currentState.state_name);

            var $items = $(
                qweb.render("FormSelection.items", {
                    states: _.without(states, currentState),
                })
            );
            var $dropdown = this.$(".dropdown-menu");
            $dropdown.children().remove();
            $items.appendTo($dropdown);
            var isReadonly = this.record.evalModifiers(this.attrs.modifiers).readonly;
            this.$("a[data-toggle=dropdown]").toggleClass(
                "disabled",
                isReadonly || false
            );
        },
    });
    fieldRegistry.add("weni_state_selection", WeniStateSelection);
    return WeniStateSelection;
});
