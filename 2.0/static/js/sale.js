window.onload = function(){

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

	// llenando los productos
	fetch("/getmyproducts", {
		method:"GET",
		credentials:"same-origin",
		headers:{
			'X-CSRF-TOKEN': getCookie('csrf_access_token'),
			"Content-Type":"application/json",
		},
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
					<td atyle="text-align:center">${products[i].stock}</td>
					<td style="text-align:center;"><img width="70px" height="70px" src="/static/img/upload/${products[i].image}" /></td>
				</tr>`
			}
		})
	// llenando los productos
	
	
	// eventos*******
	
	const btnToSale = document.getElementById("btn-sale-product").addEventListener("click", (ev)=>{
		ev.preventDefault()
		const container = document.getElementById("container")
		const popuSaleProduct = document.getElementById("popup-sale-product")
		const childNodes = container.getElementsByTagName('*');
		for (var node of childNodes) {
			node.disabled = true;
		}
		container.classList.add("opacity")
		popuSaleProduct.classList.remove("ocult")
		popuSaleProduct.classList.add("popup-sale-product")
	})

	const form = document.getElementById("form-sale-product")
	form.addEventListener("submit", ev=>{
		ev.preventDefault()
		fetch("/register_product",{
			method:"POST",
			credentials:"same-origin",
			headers:{
				'X-CSRF-TOKEN': getCookie('csrf_access_token'),
			},
			body:new FormData(ev.target)
		})
			.then(response => {
				if(response.status == 401){
					alert("Debe iniciar sesion")
					window.location.href = "/"
				}
				return response.json()
			})
			.then(data => {
				alert(data.message)
				if(data.status == 200){		
					window.location.href = window.location.href;
					//document.getElementById("cancel-sale-button").click()
				}
			})
	})

	const btnCancelSale = document.getElementById("cancel-sale-button")
	btnCancelSale.addEventListener("click", (ev)=>{
		ev.preventDefault()
		document.getElementById("description").value=""
		document.getElementById("price").value=""
		document.getElementById("stock").value=""
		document.getElementById("image").value=""
		const container = document.getElementById("container")
		const popuSaleProduct = document.getElementById("popup-sale-product")
		const childNodes = container.getElementsByTagName('*');
		for (var node of childNodes) {
			node.disabled = false;
		}
		container.classList.remove("opacity")
		popuSaleProduct.classList.add("ocult")
		popuSaleProduct.classList.remove("popup-sale-product")

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

