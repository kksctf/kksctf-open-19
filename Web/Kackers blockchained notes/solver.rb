require "net/http"
require "digest"

$x = ''
$curr = 'c3e97dd6e97fb5125688c97f36720cbe'
$ans = []
def bruter(bytes)
    (1..10000000).each do |x| 
        if Digest::MD5.hexdigest(x.to_s).chars.last(4).join == bytes
         $x = x
         puts "got needed chislo #{x}" 
         break
        end
     end
end

def fang(hash)
    begin
    puts "fanging #{hash}" 
    puts $ans && exit(0) if hash.nil? 
    return `fang --hash #{hash}`.scan(/is '([a-z0-9]{4})/)[0][0]
    rescue NoMethodError => e
        puts "go to hashkiller and do it manualluy: #{hash}"
        puts "now u are on #{$curr}"
        puts "fuk humans, i refresh capthca by myself"
        main
        end
end

def main
    loop do
        begin 
        uri = URI("http://open.kksctf.ru:20005/#{$curr}.php") #ch IP
        x = Net::HTTP.get_response(uri)
        cookies = x['set-cookie'].split('; ')[0]
        bytes = fang(x.body.scan(/value="([a-z0-9]{32})/)[0][0])
        bruter(bytes)
        uri = URI("http://open.kksctf.ru:20005/#{$curr}.php") #ch IP
        http = Net::HTTP.new(uri.host, uri.port)   
        request = Net::HTTP::Post.new(uri)
        request.set_form_data('s' => 'OK', 'ch' => "#{$x}")
        request['Cookie'] = cookies
        response = http.request(request)
        puts dig = response.body.scan(/<br><br>([\w\.\,]{1,})<br>/)[0][0]
        puts "no secrets" && exit(0) if dig.nil?
        $ans << dig
        puts $curr = Digest::MD5.hexdigest("#{$curr+dig}")
        print $ans.join(" ")
        print "\n"
        puts $ans && exit(0) if response.code != 200.to_s
        rescue => e
            print $ans.join(" ")
            exit(0)
        end
    end
end

main
