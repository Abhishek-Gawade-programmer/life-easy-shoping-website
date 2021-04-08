
const s1 =document.getElementById('s1');
const s2 =document.getElementById('s2');
const s3 =document.getElementById('s3');
const s4 =document.getElementById('s4');
const s5 =document.getElementById('s5');
const message =document.getElementById('notification');
const message_text =document.getElementById('message-text');
const save_post =document.getElementById('save-post');





const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const rate_from =document.getElementsByClassName('rate-form')[0];

var  initial_rate=0;




const arr=[s1,s2,s3,s4,s5]

function clear () {
	arr.forEach(item => $(item).removeClass("checked"));
	
}


function set_rating(rate_number){
	clear()

	for (rate in arr) {	
		if ( rate < rate_number) {
				// let x =document.getElementById('s'+toString(parseInt(rate)+1));
				 $(arr[rate]).addClass('checked');

			};



	}
}


arr.forEach(item => item.addEventListener('mouseover',
	(event)=>{

		
		set_rating(event.target.id[1])



	}

	))

arr.forEach(item => item.addEventListener('click',
	(event)=>{
		initial_rate=event.target.id[1]
		message.innerHTML = '<div class="alert alert-info alert-dismissible fade show" role="alert"> Sucessfully Rated '+ event.target.id[1]+ '</div>'

	})

)

save_post.addEventListener('click',	(event)=>{

		
		$.ajax(

		{

			type:'POST',

			url:'/rate_comment_on_product/',


			data:{

				'csrfmiddlewaretoken':csrftoken,

					'slug':rate_from.id,

					'num_rate':initial_rate,
					'message':message_text.value

				},
				
				success :function(response){
					location.reload()
					
				}
		})



		

	})
 













    




