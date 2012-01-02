(ns juno.lexer)

(defn skip-whitespace [text]
  (loop [text text]
    (if (and (seq text) (Character/isWhitespace (first text)))
      (recur (rest text))
      (apply str text))))

(defn next-id-or-keyword [source]
  (loop [[ch & remaining :as source] source, token []]
    (if (and ch (Character/isLetterOrDigit ch))
      (recur remaining (conj token ch))
      (let [token (apply str token)]
        [(cond (= "defn" token) [:defn]
               (= "fn" token) [:fn]
               (= "let" token) [:let]
               (= "if" token) [:if]
               (= "else" token) [:else]
               (= "loop" token) [:loop]
               (= "break" token) [:break]
               :else [:identifier token]) (apply str source)]))))

(defn number-token [token]
  (let [string (apply str token)]
   (if (.contains string ".")
     [:double (Double/parseDouble string)]
     [:int (Integer/parseInt string)])))

(defn next-number [source]
  (loop [[ch & remaining :as source] source, token []]
    (if (and ch (or (Character/isDigit ch) (= \. ch)))
      (recur remaining (conj token ch))
      [(number-token token) (apply str source)])))

(defn next-comment [source]
  (loop [[ch & remaining :as source] source, comment []]
    (if (or (not ch) (= \newline ch))
      [[:comment (apply str comment)] (apply str source)]
      (recur remaining (conj comment ch)))))

(defn next-token [source]
  (let [[ch & remaining] source]
    (cond
     (Character/isLetter ch) (next-id-or-keyword source)
     (or (Character/isDigit ch) (= \. ch)) (next-number source)
     (= \# ch) (next-comment source)
     :else [[ch] (apply str remaining)])))

(defn tokenize [source]
  (loop [source (skip-whitespace source) tokens []]
    (if (seq source)
      (let [[token remaining] (next-token source)]
        (recur (skip-whitespace remaining) (conj tokens token)))
      tokens)))
