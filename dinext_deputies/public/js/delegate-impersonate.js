$(document).on('app_ready', function () {
    if (frappe.session.user === "Guest") return;
    
    frappe.router.once('change', add_delegation_menu );
    $(document).one("form-load form-rename", add_delegation_menu );
});

const add_delegation_menu = () => {    
    let current_page = frappe.ui.pages[ Object.keys( frappe.ui.pages )[0] ];

    if ( current_page ) {
        frappe.router.off('change', add_delegation_menu );
        $(document).off("form-load form-rename", add_delegation_menu );
    } else {
        return;
    }

    $('.delegation-menu').remove();

    frappe.call({
        method: "dinext_deputies.api.get_delegatable_users",
        callback: function (r) {
            const users = r.message || [];

            if ( users.length ) {
                let group = current_page.add_custom_button_group(__("Войти как.."), "users", $(".navbar-collapse form"));
                group.parent().addClass('delegation-menu');
                group.parent().find(".visible-xs").removeClass("visible-xs").addClass("d-md-none");
                group.parent().css("position","relative");

                users.forEach(user => {
                    current_page.add_custom_menu_item(group, user.full_name, () => {
                        frappe.prompt({
                            fieldname: "reason",
                            fieldtype: "Small Text",
                            label: __("Комментарий"),
                            reqd: 1,
                            description: __("Будет отправлено уведомление пользователю")
                        }, (values) => {
                            frappe.call({
                                method: "frappe.core.doctype.user.user.impersonate",
                                args: { user: user.name, reason: values.reason },
                                callback: () => location.reload()
                            });
                        }, `Войти как ${user.full_name}`, "Продолжить");
                    }, true);
                });
            }
        }
    });
}