//
//  LoginViewController.swift
//  Uploader
//
//  Created by wei yi on 7/07/2016.
//  Copyright (c) 2016 wei yi. All rights reserved.
//


import UIKit

class LoginViewController: UIViewController{
    @IBOutlet weak var Username: UITextField!
    @IBOutlet weak var Password: UITextField!
    
    
    //Send Request with information to the server.
    @IBAction func Login(sender: AnyObject) {
        let username:NSString = Username.text
        let password:NSString = Password.text
        if(username==""||password==""){
            let alertView:UIAlertView = UIAlertView()
            alertView.title = "Sign in Failed!"
            alertView.message = "Please enter Username and Password"
            alertView.delegate = self
            alertView.addButtonWithTitle("OK")
            alertView.show()
        }
        else if(username=="123"&&password=="123"){
            self.performSegueWithIdentifier("login", sender: self)
        }else{
            let error_msg = "Invalid username or password!"
            let alertView:UIAlertView = UIAlertView()
            alertView.title = "Sign in Failed!"
            alertView.message = error_msg as String
            alertView.delegate = self
            alertView.addButtonWithTitle("OK")
            alertView.show()
        }
        
    }
    
    override func touchesBegan(touches: Set<UITouch>, withEvent event: UIEvent?) {
        self.view.endEditing(true)
    }
}
