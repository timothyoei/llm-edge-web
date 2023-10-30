import React from 'react'
import './login.css'
import { useState } from "react";

const Login = () =>{
    const [action, setAction] = useState("Login")

    return (
        <div className = 'container'> 
            <div className = ' header'>
                <div className = 'text'>{action}</div>
                <div className = 'underline'></div>
            </div>
            <div className = 'inputs'>
                <div className = 'input'>
                    <input type ="text" placeholder='Username'/>
                </div>
                <div className = 'input'>
                    <input type ="password" placeholder='Password'/>
                </div>
            </div>
        
            <div className = 'submit-container'>
                <div className = {action === "Login" ? "submit gray" : "submit"} onClick={()=>{setAction("Login")}}>Login</div>
                <div className = {action === "SignUp" ? "submit gray" : "submit"} onClick= {()=>{setAction("SignUp")}}>SignUp</div>
            </div>
            <div className = 'forgot-password'>Forgot Password? <span>Click Here!</span></div>

        </div>
    )
}

export default Login