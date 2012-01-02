(ns juno.test.parser
  (:use [juno.parser])
  (:use [clojure.test]))

(deftest parse-test
  (is (= nil (parse []))))
