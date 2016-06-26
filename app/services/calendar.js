var CLIENT_ID = '1024232874468-ptfrdrq0s1tns1mrfeahb1b1jbnbmrgn.apps.googleusercontent.com';

      var SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"];

      window.onload = function () {
        handleAuthClick();
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

        if (authResult && !authResult.error) {
          // Hide auth UI, then load client library.
          loadCalendarApi();
          // console.log("whaaat?");
          // listUpcomingEvents();
        } else {
          // Show auth UI, allowing the user to initiate authorization by
          // clicking authorize button.

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

           /*print out the results of users calendar response*/

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


        console.log(t_min);
        console.log(t_max);

        request.execute(function(resp) {
          var events = resp.items;
          // appendPre('The up comming events in your calendar are:'+ '\n'+'\n');
          //
          //
          //
          // if (events.length > 0) {
          //   for (i = 0; i < events.length; i++) {
          //
          //     var event = events[i];
          //     var when = event.start.dateTime;
          //
          //     if (!when) {
          //       when = event.start.date;
          //     }
          //     appendPre(i+1+' '+ event.summary + ' ('+' '+ when +' '+ ')' + '\n');
          //   }
          // } else {
          //   appendPre('No upcoming events found.');
          // }

          console.log(events);
          // $ = jquery();
          var test = document.getElementById("ScheduleCtr");
          var scope = angular.element(test).scope();
          // console.log(test);
          scope.$apply(function(){
            scope.plans = events;
          })
        });
      }

          /* this will return the out put to body as its next node */

      // function appendPre(message) {
      //   var pre = document.getElementById('output');
      //   var textContent = document.createTextNode(message + '\n');
      //   pre.appendChild(textContent);}
