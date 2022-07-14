window.onload = function(){
	fetch("/getproductstosale",{
		method:"GET",
		credentials:"same-origin",
		headers:{
			'X-CSRF-TOKEN': getCookie('csrf_access_token'),
			"Content-Type":"application/json",
		}
	})
		.then(response=>{
			if(response.status == 401){
				alert("Debe Iniciar Sesion")
				window.location.href = "/"
			}
			console.log(response)
			return response.json()
		})
		.then(data=>{
			const content = document.getElementById("content-container")
			console.log(content)
			products = data.products
			for(let i=0; i<products.length; i++){
				content.innerHTML += `\
				<div class="item">
					<div class="item-data">
						<img width="70px" height="70px" src="/static/img/upload/${products[i].image}" />
					</div>
					<div class="item-data">
						<div>Descripci&oacute;n:&nbsp;</div>
						<div>${products[i].description}</div>
					</div>
					<div class="item-data">
						<div>Precio:&nbsp;</div>
						<div>${products[i].price}</div>
					</div>
					<div class="item-data">
						<div>Stock:&nbsp;</div>
						<div>${products[i].stock}</div>
					</div>
					<div class="item-data">
						<button class="bttn-add-car" id="${products[i].id}">Agregar Al carrito</button>
					</div>
				</div>`
			}
			const buttons_add = document.getElementsByClassName("bttn-add-car")
			for(let i=0; i<buttons_add.length; i++){
				console.log("asddas")
				buttons_add[i].addEventListener("click", ev => {
					console.log("asdasd")
					fetch("/addtocar",{
						method:"POST",
						credentials:"same-origin",
						headers:{
							'X-CSRF-TOKEN': getCookie('csrf_access_token'),
							"Content-Type":"application/json",
						},
						body:JSON.stringify({
							id:ev.target.id,
						})
					})
						.then(response => {
							if(response.status == 401){
								alert("Debe Iniciar Sesion")
								window.location.href = "/"
							}
							return response.json()
						})
						.then(data =>{
							alert(data.message)
						})
					
				})
			}
		})
	

	document.getElementById("btn-logout").addEventListener("click", ev => {
		ev.preventDefault()
		fetch("/logout",{
			method:"POST",
			headers:{
				'X-CSRF-TOKEN': getCookie('csrf_access_token'),
			}
		})
		.then(response=>response.json())
			.then(data => {
				window.location.href="/"
			})
	})	
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

