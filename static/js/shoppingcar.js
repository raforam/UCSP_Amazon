window.onload = () =>{
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

	// obteniendo my shopping car
	fetch("/getmyshoppingcar",{
		method:"GET",
		credentials:"same-origin",
		headers:{
			'X-CSRF-TOKEN': getCookie('csrf_access_token'),
			"Content-Type":"application/json",
		}
	})
	.then(reponse => {
		if(reponse.status == 401){
			alert("Debe iniciar sesion")
			window.location.href = "/"
		}
		return reponse.json() 
	})
	.then(data => {
		const tableOfProducts = document.getElementById("products-body")
		products = data.products
		console.log(products)
		for(let i=0; i<products.length; i++){
			tableOfProducts.innerHTML += `\
			<tr>
				<td style="text-align:center">${products[i].description}</td>
				<td style="text-align:center">${products[i].price}</td>
				<td style="text-align:center">${products[i].stock}</td>
				<td style="text-align:center;"><img width="70px" height="70px" src="/static/img/upload/${products[i].image}" /></td>
				<td style="text-align:center;"><button id="${products[i].id}" class="delete">Quitar</button></td>
			</tr>`
		}
		const buttons = document.getElementsByClassName("delete")
		for(let i=0; i<buttons.length; i++){
			buttons[i].addEventListener("click", ev => {
				const container = document.getElementById("container")
				const popup = document.getElementById("popup-delete-car")
				const childNodes = container.getElementsByTagName('*');
				for (var node of childNodes) {
					node.disabled = true;
				}
				console.log(ev.target.id)
				document.getElementById("product_id").value = ev.target.id
				container.classList.add("opacity")
				popup.classList.remove("ocult")
				popup.classList.add("popup-delete-car")
			})
		}
	})
	

	document.getElementById("form-delete-car").addEventListener("submit", ev =>{
		ev.preventDefault()
		fetch("/delete_item_car",{
			method:"DELETE",
			credentials:"same-origin",
			headers:{
				'X-CSRF-TOKEN': getCookie('csrf_access_token'),
				'Content-Type':"application/json"
			},
			body:JSON.stringify({
				id: document.getElementById("product_id").value
			})
		})

		.then(response =>{
			if(response.status == 401){
				alert("Debes Iniciar Sesion")
				window.location.href = "/"
			}
			return response.json()
		})
		.then(data => {
				alert(data.message)
				if(data.status === 200)
					window.location.href = window.location.href
		})
	})

	document.getElementById("cancel-operation").addEventListener("click", () => {
		document.getElementById("product_id").value = ""
		const container = document.getElementById("container")
		const popup = document.getElementById("popup-delete-car")
		const childNodes = container.getElementsByTagName('*');
		for (var node of childNodes) {
			node.disabled = false;
		}
		container.classList.remove("opacity")
		popup.classList.add("ocult")
		popup.classList.remove("popup-delete-car")
		
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
