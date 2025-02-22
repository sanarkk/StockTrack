import axios from "axios"; 
const BASE_URL = "http://127.0.0.1:8001" //should be in an env file 
const GENERIC_TOKEN = "1234"

const client = axios.create({
	BASE_URL, }) 


client.interceptors.request.use((config)=>{
	try{
		let token = window.localStorage.getItem("token"); 
		// if(token && typeof(token) === "string" ){
		// 	//config.headers["auth"] = token; 
		// }
		// else{
		// 	//store generic token in request headers
		// 	//config.headers["token"] = GENERIC_TOKEN; 
			
    	
		
		// } 
		config.headers['Content-Type'] = 'application/json'; 
		return config; 
		
	}
	catch (error) {
		return Promise.reject(error); 
	}
}); 

// client.interceptors.response.use((res)=>{
// 	try{
// 		res.headers
// 	}
// 	catch(error){
// 		return Promise.reject(error)
// 	}

// })


export const get = async(route)=>{
	try{
		const res = await client.get(route); 
		return {data:res.data, status_code: res.status, error:res.status>=400?res.data.detail.msg:null}; 
	}
	catch(error){
		return {data:null, status_code:1, error:error}; 
	}
}


export const post = async(route, data)=>{
	try{
		console.log(route)
		const res = await client.post(`${route}`,data); 
		return {data:res.data, status_code: res.status, error:res.status>=400?res.data.detail.msg:null}; 
	}
	catch(error){
		return {data:null, status_code:1, error:error}; 
	}

}

export const put = async(route, data)=>{
	try{
		const res = await client.put(`${route}`,data); 
		return {data:res.data, status_code: res.status, error:res.status>=400?res.data.detail.msg:null}; 
	}
	catch(error){
		return {data:null, status_code:1, error:error}; 
	}

}

export const _delete = async(route)=>{
	try{
		const res = await client.delete(`${route}`); 
		return {data:res.data, status_code: res.status, error:res.status>=400?res.data.detail.msg:null}; 
	}
	catch(error){
		return {data:null, status_code:1, error:error}; 
	}
}


