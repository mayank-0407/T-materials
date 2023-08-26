let main_id;
function editeval(id,eval_type,eval_room,eval_information){
    document.getElementById("eval_type").value = eval_type;
    document.getElementById("eval_room").value = eval_room;
    document.getElementById("eval_information").value = eval_information;
    document.getElementById("eval_sub").value = id;
}
// function sendReqToServer(statuss, zone ,monitorCount,id){

    
//     serializedData={'statuss' : statuss, 'desk_id':id,'zone' : zone, 'monitorCount' : monitorCount};
//     console.log(serializedData);
    

//     $.ajax({
//         type: 'GET',
//         url: "./submit",
//         data: serializedData,
//         success: function (response) {
//             console.log("Desk has been updated.")
//             location.reload()
//         },
//         error: function (response) {
//             location.reload()
//             alert(response["responseJSON"]["error"]);
//         }
//     })
// }

// submit_edit.addEventListener('click', ()=>{

//     statuss=document.getElementById('status_id').value;
//     console.log(statuss)
//     zone=document.getElementById('zone_id').value;
//     monitorCount=document.getElementById('deskcount_id').value;
//     sendReqToServer(statuss, zone ,monitorCount,main_id);
// })