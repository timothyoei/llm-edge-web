import React from 'react'
import './signup.css'
import { useState } from "react";
import { Link } from "react-router-dom";

const Signup = () =>{
    const [action, setAction] = useState("Sign Up")

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
                <div className = 'input'>
                    <input type ="password" placeholder='Confirm Password'/>
                </div>
                <div className = 'input'>
                    <input type ="email" placeholder='Email'/>
                </div>
            </div>
        
            <div className = 'submit-container'>
                <div className = {"submit"} onClick={()=>{ setAction("Sign Up")}}>Sign Up</div>
                
            </div>
            <div className = 'NoAccount'>Already have an account?<br></br><span><Link to = "/">Login here!</Link></span></div>
            

        </div>
    )
}

export default Signup 