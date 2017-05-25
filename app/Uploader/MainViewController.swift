//
//  ViewController.swift
//  Uploader
//
//  Created by wei yi on 5/07/2016.
//  Copyright (c) 2016 wei yi. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

    //Description textfield
    @IBOutlet weak var Description: UITextField!
    //Image View
    @IBOutlet weak var photoImageView: UIImageView!
    
    @IBAction func buttonPressed(sender: UIButton) {
        let title = sender.titleForState(.Normal)!
        if(title=="Choose an image"){
            let photoPicker         = UIImagePickerController()
            photoPicker.delegate    = self
            photoPicker.sourceType  = .PhotoLibrary
            self.presentViewController(photoPicker, animated: true, completion: nil)
        }else if(title=="Submit"){
            
            Description.text="WTF?"
        }
        
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        self.view.addSubview(photoImageView)
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    //Open an image picker using build-in gallary
    func imagePickerController(picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : AnyObject]) {
        photoImageView.image = info[UIImagePickerControllerOriginalImage] as? UIImage
        self.dismissViewControllerAnimated(false, completion: nil)
    }
    
    //Assign first responser to the touch
    override func touchesBegan(touches: Set<UITouch>, withEvent event: UIEvent?) {
        self.view.endEditing(true)
    }


}

