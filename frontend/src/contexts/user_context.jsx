import { get,put,_delete, post, decodetoken } from "../api/api";
import { createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router";
import toast from "react-hot-toast";


export const UserContext = createContext(); 
const UserContextProvider = ({children})=>{
    const navigate = useNavigate(); 
    const [username, setUsername] = useState("user"); 
    const [user_id, set_user_id] = useState("user_id"); 
    const [interested_in, set_interested_in] = useState([]); 
    
    useEffect(()=>{
        refresh_user(); 
    },[])

    const register = async (payload)=>{
        toast.promise(
            async ()=>{
            payload["chat_id"] = ""; 
            payload["interested_in"] = []; 
            payload["date"] = new Date(); 
            const res = await post("register",payload); 
            if(res.data){
                toast.success("Registration successful")
                setUsername(res.data.username) 
                set_user_id(res.data.user_id)
                let login_payload = {}; 
                login_payload["username"] = payload.username 
                login_payload["password"] = payload.password
                login(login_payload);     
            }
            else{
                toast.error(res.error)
            }
           }, 
            {
                loading: 'Registering you',
                error:"something went wrong, please try again later"
            }
        )
    }; 

    const logout = async ()=>{
        window.localStorage.removeItem("token")
        navigate("/",{replace:true})
        toast.success("logged out")
    }

    const login = async (payload)=>{
        toast.promise(
            async () => {
                const res = await post("token",payload); 
                if(res.data){
                        window.localStorage.setItem("token",res.data.access_token)
                        setUsername(res.data.username); 
                        set_user_id(res.data.user_id); 
                        set_interested_in(res.data.interested_in); 
                        navigate("/home")
                }
                else{
                    toast.error(res.error)
                }
            },
            {
              loading: 'Logging you in',
              error:"something went wrong, please try again later"
            }
        );
    };

    const refresh_user = async()=>{
        const token_user_data = decodetoken(); 
        if(token_user_data){
            const res = await get(`get_user_info/?username=${token_user_data.username}`)
            if(res.data){
                setUsername(res.data.username); 
                set_user_id(res.data.user_id); 
                set_interested_in(res.data.interested_in); 
            }
            else{
                navigate("/")
            }
        }
        else{
            navigate("/")
        }
    }
    
    
    return(
        <UserContext.Provider
            value={{
                login, register, username, user_id, interested_in, logout
            }}
        >
            {children}
        </UserContext.Provider>
    )


}




export default UserContextProvider


