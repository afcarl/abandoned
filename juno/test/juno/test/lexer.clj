(ns juno.test.lexer
  (:use [juno.lexer])
  (:use [clojure.test]))

(deftest skip-whitespace-test
  (is (= "abc" (skip-whitespace "  \n \tabc")))
  (is (= "abc" (skip-whitespace "abc"))))

(deftest next-id-or-keyword-test
  (let [[token source] (next-id-or-keyword "defn foo(n)")]
    (is (= token [:defn]))
    (is (= source " foo(n)")))
  (let [[token source] (next-id-or-keyword "let i = 2")]
    (is (= token [:let]))
    (is (= source " i = 2")))
  (let [[token source] (next-id-or-keyword "if x > y{")]
    (is (= token [:if]))
    (is (= source " x > y{")))
  (let [[token source] (next-id-or-keyword "else { 7")]
    (is (= token [:else]))
    (is (= source " { 7")))
  (let [[token source] (next-id-or-keyword "loop {\ni = i + 1\nbreak\n}")]
    (is (= token [:loop]))
    (is (= source " {\ni = i + 1\nbreak\n}")))
  (let [[token source] (next-id-or-keyword "break\n}")]
    (is (= token [:break]))
    (is (= source "\n}")))
  (let [[token source] (next-id-or-keyword "fn (x) x")]
    (is (= token [:fn]))
    (is (= source " (x) x")))
  (let [[token source] (next-id-or-keyword "foobar = 19\nbaz()")]
    (is (= token [:identifier "foobar"]))
    (is (= source " = 19\nbaz()"))))

(deftest number-token-test
  (is (= [:double 17.4] (number-token "17.4")))
  (is (= [:double 28.0] (number-token "28.")))
  (is (= [:double 0.19] (number-token ".190")))
  (is (= [:int 29] (number-token "29")))
  (is (thrown? NumberFormatException (number-token "17.48a9.2"))))

(deftest next-number-test
  (let [[token source] (next-number "29.486\nlet i = 20")]
    (is (= token [:double 29.486]))
    (is (= source "\nlet i = 20"))))

(deftest next-comment-test
  (let [[token source] (next-comment "#this is a comment!\nlet j = k# so is this!")]
    (is (= token [:comment "#this is a comment!"]))
    (is (= source "\nlet j = k# so is this!"))))

(deftest next-token-test
  (let [[token source] (next-token "#this is a comment!\nlet j = k# so is this!")]
    (is (= token [:comment "#this is a comment!"]))
    (is (= source "\nlet j = k# so is this!")))
  (let [[token source] (next-token "29.486\nlet i = 20")]
    (is (= token [:double 29.486]))
    (is (= source "\nlet i = 20")))
  (let [[token source] (next-token "loop {\ni = i + 1\nbreak\n}")]
     (is (= token [:loop]))
     (is (= source " {\ni = i + 1\nbreak\n}")))
   (let [[token source] (next-token "+ (foo(n))")]
     (is (= token [\+]))
     (is (= source " (foo(n))"))))

(deftest tokenize-test
  (let [tokens (tokenize "# just a demo function\ndefn foo(a, b) {\n
if a > -3.79 {\nlet c = a - b\nlet i = 0#counter\n\nloop {\nif i == 5 {\n
break\n}\n\nc = c + i\ni = i + 1\n}\n\nc\n} else {\nbaz(a + b)\n}\n}")]
    (is (= tokens
           [[:comment "# just a demo function"]
            [:defn] [:identifier "foo"]
            [\(] [:identifier "a"] [\,] [:identifier "b"] [\)] [\{]
            [:if] [:identifier "a"] [\>] [\-] [:double 3.79] [\{]
            [:let] [:identifier "c"] [\=] [:identifier "a"] [\-] [:identifier "b"]
            [:let] [:identifier "i"] [\=] [:int 0] [:comment "#counter"]
            [:loop] [\{]
            [:if] [:identifier "i"] [\=] [\=] [:int 5] [\{] [:break] [\}]
            [:identifier "c"] [\=] [:identifier "c"] [\+] [:identifier "i"]
            [:identifier "i"] [\=] [:identifier "i"] [\+] [:int 1]
            [\}]
            [:identifier "c"]
            [\}] [:else] [\{]
            [:identifier "baz"] [\(] [:identifier "a"] [\+] [:identifier "b"] [\)]
            [\}]
            [\}]]))))
