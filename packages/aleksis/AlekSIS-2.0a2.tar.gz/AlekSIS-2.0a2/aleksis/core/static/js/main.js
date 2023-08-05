$(document).ready( function () {
    $("dmc-datetime input").addClass("datepicker");
    $("[data-form-control='date']").addClass("datepicker");
    $("[data-form-control='time']").addClass("timepicker");

    // Initialize sidenav [MAT]
    $(".sidenav").sidenav();

    // Initialize datepicker [MAT]
    $('.datepicker').datepicker({
        format: get_format('SHORT_DATE_FORMAT').toLowerCase().replace('d', 'dd').replace('m', 'mm').replace('y', 'yyyy'),
        // Pull translations from Django helpers
        i18n: {
            months: calendarweek_i18n.month_names,
            monthsShort: calendarweek_i18n.month_abbrs,
            weekdays: calendarweek_i18n.day_names,
            weekdaysShort: calendarweek_i18n.day_abbrs,
            weekdaysAbbrev: calendarweek_i18n.day_abbrs.map(([v])=> v),

            // Buttons
            today: gettext('Today'),
            cancel: gettext('Cancel'),
            done: gettext('OK'),
        },

        // Set monday as first day of week
        firstDay: get_format('FIRST_DAY_OF_WEEK'),
        autoClose: true
    });

    // Initialize timepicker [MAT]
    $('.timepicker').timepicker({
        twelveHour: false,
        autoClose: true,
        i18n: {
            cancel: 'Abbrechen',
            clear: 'Löschen',
            done: 'OK'
        },
    });

    // Initialize tooltip [MAT]
    $('.tooltipped').tooltip();

    // Initialize select [MAT]
    $('select').formSelect();

    // Initalize print button
    $("#print").click(function () {
        window.print();
    });

    // Initialize Collapsible [MAT]
    $('.collapsible').collapsible();

    // Initialize FABs [MAT]
    $('.fixed-action-btn').floatingActionButton();

    // Initialize Modals [MAT]
    $('.modal').modal();

    // Intialize Tabs [Materialize]
    $('.tabs').tabs();

    $('table.datatable').each(function (index) {
        $(this).DataTable({
            "paging": false
        });
    });

    // Initialise auto-completion for search bar
    window.autocomplete = new Autocomplete({minimum_length: 2});
    window.autocomplete.setup();

    // Initialize text collapsibles [MAT, own work]
    $(".text-collapsible").addClass("closed").removeClass("opened");

    $(".text-collapsible .open-icon").click(function (e) {
        var el = $(e.target).parent();
        el.addClass("opened").removeClass("closed");
    });
    $(".text-collapsible .close-icon").click(function (e) {
        var el = $(e.target).parent();
        el.addClass("closed").removeClass("opened");
    });
});
