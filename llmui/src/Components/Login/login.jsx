import React from 'react'
import './login.css'
import { useState } from "react";
import { Link } from "react-router-dom";

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
                    <div className = {"submit"} onClick={()=>{ setAction("Login")}}>Login</div>
                    
                </div>
                <div className = 'NoAccount'>Don't have an account?<br></br><span><Link to = "/SignUp">Sign Up here!</Link></span></div>
                <div className = 'forgot-password'>Forgot Password? <span>Click Here!</span></div>

            </div>
        
    )
}

export default Login