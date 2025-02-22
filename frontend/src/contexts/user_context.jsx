import { get,put,_delete, post } from "../api/api";
import { createContext, useState } from "react";
import { useNavigate } from "react-router";
import toast from "react-hot-toast";


export const UserContext = createContext(); 
const UserContextProvider = ({children})=>{
    const navigate = useNavigate(); 
    const [username, setUsername] = useState("user"); 
    const [user_id, set_user_id] = useState("user_id"); 
    const [interested_in, set_interested_in] = useState([]); 
    


    const register = async (payload)=>{
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
        else if (res.status_code != 1){
            toast.error(res.error)
        }
        else{
            toast.error("something occured during login, try again please")
        }
    }; 

    const login = async (payload)=>{
        toast.promise(
            async () => {
                const res = await post("token",payload); 
                if(res.data){
                    navigate("/home")

                }
                else if (res.status_code != 1){
                    toast.error(res.error)
                }
                else{
                    toast.error("something occured during login, try again please")
                }
            },
            {
              loading: 'Logging you in',
            }
        );
    };
    
    
    return(
        <UserContext.Provider
            value={{
                login, register, username, user_id, interested_in
            }}
        >
            {children}
        </UserContext.Provider>
    )


}




export default UserContextProvider


