import webview

# We embed HTML, CSS, and JS directly so it compiles into a single file
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aesthetic Calculator</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #fbc5d8 0%, #d8b4f8 100%);
            overflow: hidden;
        }

        /* Glassmorphism card */
        .calculator {
            width: 340px;
            background: rgba(255, 255, 255, 0.45);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 30px;
            box-shadow: 0 15px 35px rgba(123, 92, 143, 0.2);
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            transform: scale(0.98);
            animation: floatIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }

        @keyframes floatIn {
            to { transform: scale(1); }
        }

        /* Screen display */
        .screen {
            background: rgba(255, 255, 255, 0.65);
            border-radius: 20px;
            padding: 20px;
            text-align: right;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.03);
            border: 1px solid rgba(255, 255, 255, 0.3);
            min-height: 110px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            overflow: hidden;
        }

        .formula {
            font-size: 1rem;
            color: #927f9e;
            margin-bottom: 5px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .display {
            font-size: 2.2rem;
            font-weight: 300;
            color: #4c325c;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            transition: all 0.1s ease;
        }

        /* Buttons Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }

        button {
            border: none;
            outline: none;
            height: 60px;
            border-radius: 18px;
            font-size: 1.3rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        }

        /* Default standard buttons */
        .btn-num {
            background: rgba(255, 255, 255, 0.8);
            color: #5c446a;
        }

        /* Operators (+, -, *, /) */
        .btn-op {
            background: rgba(242, 203, 233, 0.8);
            color: #8c557d;
        }

        /* Action buttons (Clear, Backspace) */
        .btn-action {
            background: rgba(220, 208, 245, 0.8);
            color: #5f4d80;
        }

        /* Equals button */
        .btn-equal {
            background: linear-gradient(135deg, #f9a8d4 0%, #c084fc 100%);
            color: white;
            grid-column: span 2;
            box-shadow: 0 5px 15px rgba(192, 132, 252, 0.4);
        }

        /* Dynamic Press & Hover Effects */
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(0,0,0,0.08);
        }

        button:active {
            transform: scale(0.9);
            filter: brightness(0.95);
        }
    </style>
</head>
<body>

    <div class="calculator">
        <div class="screen">
            <div id="formula" class="formula"></div>
            <div id="display" class="display">0</div>
        </div>
        
        <div class="grid">
            <button class="btn-action" onclick="clearAll()">C</button>
            <button class="btn-action" onclick="backspace()">⌫</button>
            <button class="btn-op" onclick="appendOp('/')">÷</button>
            <button class="btn-op" onclick="appendOp('*')">×</button>

            <button class="btn-num" onclick="appendNum('7')">7</button>
            <button class="btn-num" onclick="appendNum('8')">8</button>
            <button class="btn-num" onclick="appendNum('9')">9</button>
            <button class="btn-op" onclick="appendOp('-')">-</button>

            <button class="btn-num" onclick="appendNum('4')">4</button>
            <button class="btn-num" onclick="appendNum('5')">5</button>
            <button class="btn-num" onclick="appendNum('6')">6</button>
            <button class="btn-op" onclick="appendOp('+')">+</button>

            <button class="btn-num" onclick="appendNum('1')">1</button>
            <button class="btn-num" onclick="appendNum('2')">2</button>
            <button class="btn-num" onclick="appendNum('3')">3</button>
            <button class="btn-equal" onclick="calculate()">=</button>

            <button class="btn-num" style="grid-column: span 2; border-radius: 18px;" onclick="appendNum('0')">0</button>
            <button class="btn-num" onclick="appendNum('.')">.</button>
        </div>
    </div>

    <script>
        let currentInput = '0';
        let previousInput = '';
        let operation = null;
        let shouldReset = false;

        // Web Audio API Synthesizer: Synthesizes a perfect "pop" sound instantly without loading files
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function playPopSound() {
            // Re-enable context if suspended (browser security policy)
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }

            const osc = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();

            osc.type = 'sine';
            
            // Pop pitch slides downward rapidly
            osc.frequency.setValueAtTime(450, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.08);

            // Volume fades out quickly
            gainNode.gain.setValueAtTime(0.18, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);

            osc.connect(gainNode);
            gainNode.connect(audioCtx.destination);

            osc.start();
            osc.stop(audioCtx.currentTime + 0.09);
        }

        function updateScreen() {
            document.getElementById('display').innerText = currentInput;
            if (operation) {
                document.getElementById('formula').innerText = `${previousInput} ${operation}`;
            } else {
                document.getElementById('formula').innerText = '';
            }
        }

        function appendNum(num) {
            playPopSound();
            if (currentInput === '0' || shouldReset) {
                currentInput = num;
                shouldReset = false;
            } else {
                // Prevent duplicate decimals
                if (num === '.' && currentInput.includes('.')) return;
                currentInput += num;
            }
            updateScreen();
        }

        function appendOp(op) {
            playPopSound();
            if (operation !== null) calculate();
            previousInput = currentInput;
            operation = op;
            shouldReset = true;
            updateScreen();
        }

        function clearAll() {
            playPopSound();
            currentInput = '0';
            previousInput = '';
            operation = null;
            shouldReset = false;
            updateScreen();
        }

        function backspace() {
            playPopSound();
            if (currentInput.length > 1) {
                currentInput = currentInput.slice(0, -1);
            } else {
                currentInput = '0';
            }
            updateScreen();
        }

        function calculate() {
            playPopSound();
            if (operation === null || shouldReset) return;
            
            let result;
            const prev = parseFloat(previousInput);
            const current = parseFloat(currentInput);

            switch (operation) {
                case '+': result = prev + current; break;
                case '-': result = prev - current; break;
                case '*': result = prev * current; break;
                case '/': result = current === 0 ? 'Error' : prev / current; break;
                default: return;
            }

            // Round float issues (e.g. 0.1 + 0.2)
            if (typeof result === 'number') {
                result = Math.round(result * 10000000) / 10000000;
            }

            currentInput = result.toString();
            operation = null;
            previousInput = '';
            shouldReset = true;
            updateScreen();
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    # Start the native window running the HTML/CSS content
    webview.create_window(
        title="Aesthetic Calculator",
        html=html_content,
        width=360,
        height=580,
        resizable=False,
        background_color='#fbc5d8'
    )
    webview.start()
