<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Empty Page</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background-color: #000;
            color: #fff;
            font-family: Georgia, serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        .message {
            font-size: 3rem;
        }
        #message {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 2s ease, transform 2s ease;
        }
        #blinkmessage {
            font-size: 3rem;
            opacity: 1;
            transform: translateY(0);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }
    </style>
</head>
<body>
    <div class="message" id="parent"> 
        <div id="blinkmessage"></div>
        <div id="message"></div>
    </div>
    <script>
        document.addEventListener("DOMContentLoaded", async () => {
            await changeText("This is an empty page.", 1000, 3000);
            await changeText("Please return to the main page.", 3000, 7000);
            await changeText("", 7000, 1500);
            document.getElementById("message").style.opacity = 1;
            document.getElementById("message").textContent = "";
            // Start typing effects after the previous messages
            document.getElementById("message").style.fontFamily= "Terminus, monospace";
            setTimeout(() => {
                likeMatrix("    ...");
                blinkText(3);
            }, 1000);

            document.getElementById("blinkmessage").style.fontFamily= "Terminus, monospace";
            document.getElementById("parent").style.display = "flex";
            document.getElementById("parent").style.textAlign = "left";
            document.getElementById("parent").style.alignItems = "flex-start;";
            document.getElementById("parent").style.justifyContent= "flex-start";
            document.getElementById("parent").style.position = "absolute";
            document.getElementById("parent").style.top = "20px";
            document.getElementById("parent").style.left = "10px";
            document.getElementById("blinkmessage").style.fontSize = "1.2rem";
            document.getElementById("message").style.fontSize = "1.2rem";
            document.getElementById("blinkmessage").style.textAlign="left";
            document.getElementById("blinkmessage").style.paddingRight="30px";
            document.getElementById("blinkmessage").textContent = "[root@redhat.local ~]$";
            setTimeout(() => {
                likeMatrix("Matrix is watching ...");
            }, 6500);
            setTimeout(() => {
                likeMatrix("        ...Run!");
                document.getElementById("message").style.transition = "opacity 0.5s ease, transform 0.5s ease";
                blinkText(5);
            }, 12000);
            setTimeout(() => {
                likeMatrix("   shutdown now");
            }, 18000);
            setTimeout(() => {
                document.getElementById("blinkmessage").textContent = "[root@redhat.local ~]$ Bye...";
                document.getElementById("message").textContent = "";
            }, 24000);
            setTimeout(() => {
                document.getElementById("blinkmessage").textContent = "";
            }, 30000);
        });

        function changeText(message, delayShow, delayHide) {
            return new Promise(resolve => {
                const handle = document.getElementById("message");

                setTimeout(() => {
                    handle.textContent = message;
                    handle.style.opacity = 1;
                    handle.style.transform = "translateY(0)";
                }, delayShow);

                if (delayHide !== 0) {
                    setTimeout(() => {
                        handle.style.opacity = 0;
                        handle.style.transform = "translateY(30px)";
                        resolve(); // Resolve the promise when the hide animation is done
                    }, delayHide);
                }
            });
        }

        function likeMatrix(message) {
            return new Promise(resolve => {
                let index = 0;
                const handle = document.getElementById("message");
                handle.textContent = ""; // Clear previous message

                const typeWriter = () => {
                    if (index < message.length) {
                        handle.textContent += message.charAt(index);
                        index++;
                        setTimeout(typeWriter, 100); // 100ms delay between characters
                    } else {
                        resolve(); // Resolve when typing effect is complete
                    }
                };
                typeWriter(); // Start typing effect
            });
        }
        function blinkText(times) {
            return new Promise(resolve => {
                const handle = document.getElementById("message");
                let blinkCount = 0;

                const blink = () => {
                    handle.style.opacity = (handle.style.opacity === "1") ? "0" : "1";
                    blinkCount++;

                    if (blinkCount < times * 2) {
                        setTimeout(blink, 500); // Blink every 500ms
                    } else {
                        handle.style.opacity = "1"; // Ensure it's visible at the end
                        resolve();
                    }
                };

                blink(); // Start blinking
            });
        }
        function wait(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
    </script>
</body>
</html>
