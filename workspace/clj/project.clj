(defproject clj "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [
		[ org.clojure/clojure "1.7.0" ]
		[ clj-webdriver "0.7.2" ]
		[ com.sikulix/sikulixapi "1.1.0" ]
		[ jxgrabkey/jxgrabkey "1.0" ]
		;[ com.sikulix/sikulixlibslux "1.1.0" ]
		]
  :main ^:skip-aot clj.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
