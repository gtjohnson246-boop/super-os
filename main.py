<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>super-os</title>
    <style>
        body {
            background-color: #0c0c0c;
            color: #cccccc;
            font-family: 'Courier New', Courier, monospace;
            padding: 20px;
            margin: 0;
            font-size: 14px;
            line-height: 1.4;
        }
        #terminal-output {
            white-space: pre-wrap;
            margin-bottom: 10px;
        }
        #input-line {
            display: flex;
            align-items: center;
        }
        #prompt {
            color: #00ff00;
            white-space: pre;
            margin-right: 5px;
        }
        #user-input {
            background: transparent;
            border: none;
            color: #ffffff;
            font-family: inherit;
            font-size: inherit;
            flex-grow: 1;
            outline: none;
            padding: 0;
        }
        .hidden {
            display: none !important;
        }
    </style>
</head>
<body>

    <div id="terminal-output"></div>
    <div id="input-line">
        <span id="prompt"></span>
        <input type="text" id="user-input" autofocus autocomplete="off" spellcheck="false">
    </div>

    <script>
        // Global variables & state
        const VALID_USERNAME = "gabeee";
        const VALID_PASSWORD = "6655";
        let loginAttempts = 5;
        let isBooted = false;
        let isAuthenticated = false;
        let isEnteringPassword = false;
        let currentUsernameInput = "";

        // Virtual File System State
        let currentPath = ["root"];
        const fileSystem = {
            "root": {
                type: "dir",
                children: {
                    "readme.txt": { type: "file", content: "Welcome to Mini-JS-OS! This is a browser-simulated file." }
                }
            }
        };

        const outputDiv = document.getElementById("terminal-output");
        const promptSpan = document.getElementById("prompt");
        const userInput = document.getElementById("user-input");

        function print(text = "") {
            outputDiv.textContent += text + "\n";
            window.scrollTo(0, document.body.scrollHeight);
        }

        function clearTerminal() {
            outputDiv.textContent = "";
        }

        function getVirtualDir(pathArray) {
            let current = fileSystem;
            for (let folder of pathArray) {
                if (current[folder] && current[folder].type === "dir") {
                    current = current[folder].children;
                } else {
                    return null;
                }
            }
            return current;
        }

        function getCWDString() {
            return "/" + currentPath.slice(1).join("/");
        }

        function updatePrompt() {
            if (!isBooted || !isAuthenticated) {
                promptSpan.textContent = "";
                return;
            }
            promptSpan.textContent = `mini-os:${getCWDString()}> `;
        }

        function showBootScreen() {
            print("=".repeat(55));
            print("  __  __ _       _        ____   ____  ");
            print(" |  \\/  (_)_ __ (_)      / __ \\ / ___| ");
            print(" | |\\/| | | '_ \\| |_____| |  | |\\___ \\ ");
            print(" | |  | | | | | | |_____| |__| | ___) |");
            print(" |_|  |_|_|_| |_|_|      \\____/ |____/ ");
            print("=".repeat(55));
            print(" Mini-JS-OS Version: 1.8.0");
            print(` Host Machine Kernel : Web Browser (${navigator.platform})`);
            print(` System Time         : ${new Date().toLocaleString()}`);
            print("-".repeat(55));
            print(" Boot Sequence Completed successfully.");
            print("=".repeat(55) + "\n");
            
            isBooted = true;
            print("--- SYSTEM AUTHENTICATION REQUIRED ---");
            print("Username: ");
            userInput.type = "text";
        }

        function showLockoutScreen() {
            const tuxArt = [
                "##########**************************##########",
                "######***************%%%%%**************######",
                "###*****************#%%%#@@****************###",
                "##****************+++==+=%@*****************##",
                "#*********++++++++++*=--=%@#*+++++++*********#",
                "********++++++++++*%#::::+%%#*++++++++********",
                "******+++++++++++*%#:....+%%@#++++++++++******",
                "********+++++++++*%=::..=%%%@%++++++++********",
                "#*********++++++=*@#::::*%%%#@++++++*********#",
                "##*************+====+===+*+==*+*************##",
                "####*************++++@@@#++++++***********####",
                "######**************#%@@%++**#**********######",
                "##########**************************##########"
            ];
            
            print("\n" + "!".repeat(46));
            print(" ".repeat(14) + "SYSTEM LOCKED!");
            print(" ".repeat(7) + "Too many failed login attempts.");
            print(" ".repeat(11) + "PLEASE CONTACT OWNER.");
            print("!".repeat(46) + "\n");
            
            tuxArt.forEach(line => print(line));
            print();
            
            // Disable terminal completely
            document.getElementById("input-line").classList.add("hidden");
            userInput.blur();
        }

        function handleAuth(input) {
            if (!isEnteringPassword) {
                currentUsernameInput = input.trim();
                print(currentUsernameInput);
                isEnteringPassword = true;
                print("Password: ");
                userInput.type = "password"; // Hide password text natively
            } else {
                let password = input.trim();
                isEnteringPassword = false;
                userInput.type = "text";

                if (currentUsernameInput === VALID_USERNAME && password === VALID_PASSWORD) {
                    print("\nAccess Granted. Welcome back, Gabeee!\n");
                    print("Type 'help' for available commands or 'exit' to quit.\n");
                    isAuthenticated = true;
                    updatePrompt();
                } else {
                    loginAttempts--;
                    print("\n[!] Invalid credentials. Access Denied.");
                    if (loginAttempts > 0) {
                        print(`You have ${loginAttempts} attempt(s) remaining.\n`);
                        print("Username: ");
                    } else {
                        showLockoutScreen();
                    }
                }
            }
        }

        function executeCommand(commandLine) {
            print(promptSpan.textContent + commandLine);
            let trimmed = commandLine.trim();
            if (!trimmed) return;

            let parts = trimmed.split(/\s+/);
            let cmd = parts[0].toLowerCase();
            let args = parts.slice(1);

            let currentDirItems = getVirtualDir(currentPath);

            switch(cmd) {
                case "exit":
                    print("Shutting down Mini-JS-OS. Goodbye!");
                    document.getElementById("input-line").classList.add("hidden");
                    break;

                case "help":
                    print("Available commands:");
                    print("  help           - Show this help message");
                    print("  pwd            - Print current working directory");
                    print("  ls             - List files and folders");
                    print("  cd <dir>       - Change directory");
                    print("  mkdir <name>   - Create a new directory");
                    print("  cat <file>     - Read and display a text file");
                    print("  search_engine  - Open Google in your web browser");
                    print("  open_downloads - Pull up your Chromebook's system file manager");
                    print("  clear          - Clear the starting screen / terminal screen");
                    print("  exit           - Exit the mini OS shell");
                    break;

                case "pwd":
                    print(getCWDString());
                    break;

                case "ls":
                    Object.keys(currentDirItems).forEach(item => {
                        let suffix = currentDirItems[item].type === "dir" ? "/" : "";
                        print("  " + item + suffix);
                    });
                    break;

                case "cd":
                    if (args.length === 0) {
                        print("Error: 'cd' requires a path argument.");
                    } else {
                        let target = args.join(" ");
                        if (target === "..") {
                            if (currentPath.length > 1) currentPath.pop();
                        } else if (currentDirItems[target] && currentDirItems[target].type === "dir") {
                            currentPath.push(target);
                        } else {
                            print(`Error: Directory '${target}' not found.`);
                        }
                    }
                    break;

                case "mkdir":
                    if (args.length === 0) {
                        print("Error: 'mkdir' requires a directory name.");
                    } else {
                        let dirName = args.join(" ");
                        if (currentDirItems[dirName]) {
                            print(`Error: '${dirName}' already exists.`);
                        } else {
                            currentDirItems[dirName] = { type: "dir", children: {} };
                            print(`Directory '${dirName}' created.`);
                        }
}
break;
case "cat":
if (args.length === 0) {
print("Error: 'cat' requires a file name.");
} else {
let fileName = args.join(" ");
if (currentDirItems[fileName] && currentDirItems[fileName].type === "file") {
print(currentDirItems[fileName].content);
} else {
print(Error: File '${fileName}' not found.);
}
}
break;
case "search_engine":
print("Opening Google in your web browser...");
window.open("https://google.com", "_blank");
break;
case "open_downloads":
print("Opening your Chromebook's file manager...");
window.open("chrome://file-manager", "_blank");
break;
case "clear":
clearTerminal();
break;
default:
print(Unknown command: '${cmd}'. Type 'help' for a list of commands.);
}
}
// Event listener for user input submission
userInput.addEventListener("keydown", function(e) {
if (e.key === "Enter") {
let inputVal = userInput.value;
userInput.value = "";
if (!isAuthenticated) {
handleAuth(inputVal);
} else {
executeCommand(inputVal);
}
updatePrompt();
}
});
// Keep input focused when clicking anywhere on screen
document.addEventListener("click", () => userInput.focus());
// Initialize App
showBootScreen();