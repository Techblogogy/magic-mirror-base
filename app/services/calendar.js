var CLIENT_ID = '1024232874468-ptfrdrq0s1tns1mrfeahb1b1jbnbmrgn.apps.googleusercontent.com';
var SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"];

window.onload = function () {
    // console.log("L");
    // handleAuthClick();
}

/*Check the user authentication */
function checkAuth() {
    gapi.auth.authorize(
    {
        'client_id': CLIENT_ID,
        'scope': SCOPES.join(' '),
        'immediate': true
    }, handleAuthResult);
}

/* function for handling authorozation of server */
function handleAuthResult(authResult) {
    auth2 = gapi.auth
    if (authResult && !authResult.error) {
        console.log("Auth");
        console.log(authResult);
        // loadCalendarApi();
    } else {
        console.log("Error");
    }
}

/*the response function to user click */
function handleAuthClick() {
    gapi.auth.authorize(
        {client_id: CLIENT_ID, scope: SCOPES, immediate: true},
        handleAuthResult
    );
    return false;
}

/*loading client library */
function loadCalendarApi() {
    gapi.client.load('calendar', 'v3', listUpcomingEvents);
}

function listUpcomingEvents() {
    var today = new Date();

    var t_min = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    var t_max = new Date(today.getFullYear(), today.getMonth(), today.getDate()+1);

    var request = gapi.client.calendar.events.list({
        'calendarId': 'primary',
        'timeMin': (t_min).toISOString(),
        'timeMax': (t_max).toISOString(),
        'showDeleted': false,
        'singleEvents': true,
        'maxResults': 15,
        'orderBy': 'startTime'
    });

    request.execute(function(resp) {
        var events = resp.items;

        console.log(events);
        var test = document.getElementById("ScheduleCtr");
        var scope = angular.element(test).scope();
        scope.$apply(function(){
            scope.plans = events;
        })
    });
}
