$(document).ready(function(){
			
			$("#add_name").click(function(){
				$(".modal-box.name").fadeIn();
				$('#dialog-box').fadeIn();
			});
			$("#add_description").click(function(){
				$(".modal-box.desc").fadeIn();
				$('#dialog-box').fadeIn();
			});
			// $("#add_description").click(function(){
			// 	$("#dialog-modal-add_description").fadeIn();
			// 	$('#dialog-box2').fadeIn();
			// });
			// $("#add_url").click(function(){
			// 	$("#dialog-modal-add_url").fadeIn();
			// 	$('#dialog-box2').fadeIn();
			// });
			$("#dialog-box,.close-X").click(function(){
				$(".modal-box").fadeOut();
				$('#dialog-box').fadeOut();
			});
			// $("#add_name_submit").click(function(){
			// 	var first_name=$("input[name=first_name]").val();
			// 	var last_name=$("input[name=last_name]").val();
			// 	console.log(first_name);
			// 	console.log($(this).data("username"));
			// 	if (first_name && last_name){
			// 		$.ajax({
			// 			url:"{%url 'accounts:profile-update' "+$(this).data("username")+"%}",
			// 			method:"get",
			// 			data:{first_name:first_name,last_name:last_name},
			// 			success:function(data){
			// 				console.log(data);
			// 			}
			// 		});
			// 	} 
			// });
		});