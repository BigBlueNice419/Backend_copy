//
//  MemoryViewController.swift
//  Memories
//
//  Created by Chris Ward on 4/13/19.
//  Copyright © 2019 Chris Ward. All rights reserved.
//

import UIKit
import os.log

class MemoryViewController: UIViewController, UITextFieldDelegate, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    //MARK: Properties
    @IBOutlet weak var titleTextField: UITextField!
    @IBOutlet weak var photoImageView: UIImageView!
    @IBOutlet weak var textTextField: UITextView!
    @IBOutlet weak var saveButton: UIBarButtonItem!
    @IBOutlet weak var scrollView: UIScrollView!
    
    var memory: Memory?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // from https://stackoverflow.com/questions/36028493/add-a-scrollview-to-existing-view
        // more help from https://stackoverflow.com/questions/27680701/how-to-create-a-cgsize-in-swift
//        scrollView.contentSize = CGSize(self.view.frame.width, self.view.frame.height+CGFloat(100)

        
        // Handle the text field's user input through delegate callbacks.
        titleTextField.delegate = self
        
        // Set up views if editting an existing Memory.
        if let memory = memory {
            navigationItem.title = memory.date
            titleTextField.text = memory.title
            photoImageView.image = memory.photo
            textTextField.text = memory.text
            
        }
        
        // Enable the Save button only if the text field has a valid Memory title.
        updateSaveButtonState()
        
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(self.keyboardWillShow(_:)),
            name: UIResponder.keyboardWillShowNotification,
            object: nil
        )
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(self.keyboardWillHide(_:)),
            name: UIResponder.keyboardWillHideNotification,
            object: nil
        )
    }
    // from https://www.raywenderlich.com/560-uiscrollview-tutorial-getting-started
    
    deinit {
        NotificationCenter.default.removeObserver(self)
    }
    
    func adjustInsetForKeyboardShow(_ show: Bool, notification: Notification) {
        let userInfo = notification.userInfo ?? [:]
        let keyboardFrame = (userInfo[UIResponder.keyboardFrameEndUserInfoKey] as! NSValue).cgRectValue
        let adjustmentHeight = (keyboardFrame.height + 20) * (show ? 1 : -1)
        scrollView.contentInset.bottom += adjustmentHeight
        scrollView.scrollIndicatorInsets.bottom += adjustmentHeight
    }
    
    @objc func keyboardWillShow(_ notification: Notification) {
        adjustInsetForKeyboardShow(true, notification: notification)
    }
    
    @objc func keyboardWillHide(_ notification: Notification) {
        adjustInsetForKeyboardShow(false, notification: notification)
    }
    
    @IBAction func hideKeyboard(_ sender: AnyObject) {
        textTextField.endEditing(true)
    }
    
    //MARK: UITextFieldDelegate
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        // Hide the keyboard
        textField.resignFirstResponder()
        return true
    }
    
    func textFieldDidEndEditing(_ textField: UITextField) {
        updateSaveButtonState()
        navigationItem.title = textField.text
    }
    
    func textFieldDidBeginEditing(_ textField: UITextField) {
        // Disable the save button while editting.
        saveButton.isEnabled = false
    }
    
    //MARK: UIImagePickerControllerDelegate
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        // Dismiss the picker if user cancels.
        dismiss(animated: true, completion: nil)
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        // the info dictionary may contain multiple image representations. The original is used.
        guard let selectedImage = info[UIImagePickerController.InfoKey.originalImage] as? UIImage
            else {
                fatalError("Expected a dictionary containing an image, but was provided the following: \(info)")
        }
        
        photoImageView.image = selectedImage
        dismiss(animated: true, completion: nil)
    }
    
    //MARK: Navigation
    
    @IBAction func cancel(_ sender: UIBarButtonItem) {
        // Depending on style of presentation (modal or push presentation), this view controller needs to be dismissed in two different ways.
        let isPresentingInAddMemoryMode = presentingViewController is UINavigationController
        
        if isPresentingInAddMemoryMode {
            dismiss(animated: true, completion: nil)
        } else if let owningNavigationController = navigationController{
            owningNavigationController.popViewController(animated: true)
        } else {
            fatalError("The MemoryViewController is not inside a navigation controller.")
        }
    }
    
    // This method lets you configure a view controller before it's presented
    override func prepare(for segue: UIStoryboardSegue, sender: Any?){
        super.prepare(for: segue, sender: sender)
        
        // Configure the destination view controller only when the save button is presed
        guard let button = sender as? UIBarButtonItem, button === saveButton else {
            os_log("The save button was not pressed, cancelling", log: OSLog.default, type: .debug)
            return
        }
        
        let title = titleTextField.text ?? ""
        let photo = photoImageView.image
        let text = textTextField.text ?? ""
        
        // Set the memory to be passed to MemoryTableViewController after the unwind segue.
        memory = Memory(title: title, photo: photo, text: text)
    }
    
    //MARK: Actions
    @IBAction func selectImageFromPhotoLibrary(_ sender: UITapGestureRecognizer) {
        
        // Hide the keyboard.
        titleTextField.resignFirstResponder()
        
        // UIImagePickerController is a view controller that lets a user pick media from their photo library.
        let imagePickerController = UIImagePickerController()
        
        // Only allow photos to be picked, not taken.
        imagePickerController.sourceType = .photoLibrary
        
        // Make sure ViewController is notified when the user picks an image.
        imagePickerController.delegate = self
        present(imagePickerController, animated: true, completion: nil)
    }
    
    //MARK: Private Methods
    private func updateSaveButtonState(){
        // Disable the save button if the text field is empty.
        let title = titleTextField.text ?? ""
        let text = textTextField.text ?? ""
        saveButton.isEnabled = !(title.isEmpty && text.isEmpty)
    }

}

