// config axios to send CSRFToken to server in X-CSRFToken header 
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = 'csrftoken';
let dialog_assign_window = null;

// service1: increment counter user by agen
function incrementCounter(button) {
    const postData = {
        agent_id: button.getAttribute('data-agent-id'),
        number_window: button.getAttribute('data-window-num')
    }
    
    const refOffice = button.getAttribute('data-office-id');
    const url = `/tcn/api/offices/${refOffice}/increment-counter/`;
    axios.post(url , postData)
        .then(function (response) {
            // Handle success, update UI with new counter value
            document.getElementById('counter-display-agent').innerText = response.data.counter;
        })
        .catch(function (error) {
            // Handle error
            console.error('Error incrementing counter:', error);
        });
}
// service2 : assign  agent to window 

function assignAgentToWindow(button) {
    const postData = {
        agent_id: button.getAttribute('data-agent-id'),
        office_id: button.getAttribute('data-office-id'),
    }
    const idSelect = `windowSelect${postData.agent_id}`
    const selectedWindow = document.getElementById(idSelect).value ;
    const idResponseAssignWindow =  `response_assign_window${postData.agent_id}`
    dialog_assign_window =  document.getElementById(idResponseAssignWindow)
    if (selectedWindow === "Select a window") {
        alert("Please select a window");
        return;
    }
    const url = `/tcn/api/windows/${selectedWindow}/assign-agent/`;

    //initit 
    dialog_assign_window.innerText = "";
    axios.post(url , postData)
        .then(function (response) {
            dialog_assign_window.classList.add("text-success");
            dialog_assign_window.innerText = response.data.message
        })
        .catch(function (error) {
            dialog_assign_window.classList.add("text-danger");
            dialog_assign_window.innerText = error.response.data.error
            console.error('Error assignAgentToWindow:', error);
        });
}

// service 3 : apply action (enable or disable ) to recieve notification from selected notifications 
function apply_notification_with_action(buttonActionNotify, action, selectedOffices, responseElement) {
    // api to consume 'api/offices/<int:id_user>/<str:action>/apply'
    if (buttonActionNotify !== undefined && buttonActionNotify !== null)
    {
        const idUser =  buttonActionNotify.getAttribute('data-client-id')
        console.log(idUser)
        console.log(action)
        const postData = {
            ref_offices: selectedOffices,
        }
        const url = `/tcn/api/offices/${idUser}/${action}/apply`;
        axios.post(url , postData)
        .then(function (response) {
            styleResponseTag(responseElement, feedback.error, feedback.success , response.data.message);
        })
        .catch(function (error) {
            styleResponseTag(responseElement, feedback.success, feedback.error , error.response.data.error);
            console.error('Error apply_notification_with_action:', error);
        });
    }
}

// delete office 
function deleteOffice(buttonConfirmDeleteOffice) {
    if (buttonConfirmDeleteOffice !== undefined && buttonConfirmDeleteOffice !== null)
    {
        const ref_office =  buttonConfirmDeleteOffice.getAttribute('data-office-ref')
        const responseElement = $(`#response-delete-office${ref_office}`)
        const url = `/tcn/api/offices/${ref_office}/delete`;
        axios.delete(url)
        .then(function (response) {
            
            if (responseElement !== undefined && responseElement !== null) {
                styleResponseTag(responseElement, feedback.error, feedback.success , response.data.message);
            }
            
        })
        .catch(function (error) {
            if (responseElement !== undefined && responseElement !== null) {
                styleResponseTag(responseElement, feedback.success, feedback.error , error.response.data.error);
            }
            console.error('Error deleteOffice:', error);
        });
    }
}
//helper function to clear the response server in <p> tag 
function clearOldData(){
    if (dialog_assign_window) {
        dialog_assign_window.innerText = "";
    }
}
// helper function 
function styleResponseTag(htmlElement, nameClassToRemove, nameClassToAdd, stringContent)
{
    if (htmlElement !== undefined && htmlElement !== null)
    {   htmlElement.removeClass(nameClassToRemove)
        htmlElement.addClass(nameClassToAdd)
        htmlElement.html(stringContent);
    }
}
const feedback = {
    success: 'text-success',
    error : 'text-danger'
}

