const seApp = Application('System Events')
const messagesApp = Application('Messages')
messagesApp.includeStandardAdditions = true;

// Run and get passed in arguments
ObjC.import('stdlib')                               // for exit

var args = $.NSProcessInfo.processInfo.arguments    
var argv = []
var argc = args.count
for (var i = 4; i < argc; i++) {
    // skip 3-word run command at top and this file's name
    argv.push(ObjC.unwrap(args.objectAtIndex(i)))  
}

const number = argv[0]
const message = argv[1]

sendNewMessage(number, message)

function sendNewMessage(number, message) {
    messagesApp.activate()
    //EDIT THIS TOO WORK ON SONOMA( tested ) , Current bug: puts number and message into number input
    // Adjust delay as necessary
    delay(0.5)
    
    seApp.keystroke('n', {using: 'command down'})
    seApp.keystroke(number)
    delay(0.25);
    seApp.keyCode(48)
    delay(0.25);
    seApp.keyCode(48)
    //USE TAB TWICE TOO GO DOWN TOO MESSAGE INPUT
    delay(0.75);
    seApp.keystroke(message)
    delay(0.5);
    seApp.keyCode(36)

    return "Done!"
}

// Should prevent app from quitting
function quit() {
    return true;
}

seApp.keyUp(59)
$.exit(0)
