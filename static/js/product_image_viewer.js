z=document.querySelectorAll('.page-item');

img=document.getElementById('product_image');

function change_img(img_url){
	img.setAttribute("src", img_url);



}


function clear_active(){
	z.forEach(item => $(item).removeClass("active"));



}




z.forEach(item => item.addEventListener('click',
	(event)=>{
		clear_active();

		$(item).addClass('active');
		change_img(item.getAttribute('data'));

	}

	));



