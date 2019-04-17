#! /usr/bin/ruby
require 'mail'
require 'yaml'
require 'date'

# You must supply these yourself.
MAILFILES = "mail_files"
MAILINFO = "#{MAILFILES}/mailinfo.yml"
RECIPIENTS = "#{MAILFILES}/recipients.yml"

##
# Holds all the recipient info in a single class and provides all the necessary functions to make an email
class Recipient
    attr_reader :name, :email, :position, :skills, :contacted, :extra

    def initialize(hash)
        @name = hash["name"]
        @email = hash["email"]
        @position = hash["position"]
        @skills = hash["skills"]
        @contacted = hash["contacted"]
        @extra = hash["extra"]
    end

    ##
    # Writes the intro to the email
    def mk_intro
        ["Kære ", "Hej ", "Goddag, "].sample + @name
    end

    ##
    # Writes the body of the email
    def mk_body
        skills = @skills.join(', ')
        skills += ", m.v." if @skills.length > 1

        body = "Jeg søger stillingen som #{@position} i jeres virksomhed.\n"
        body += "Jeg føler min erfaring inden for brugen af #{skills} kunne gavne jer.\n" unless @skills.nil?
        body += "#{@extra}\n" unless @extra.nil?
        return body
    end

    ##
    # Writes the outro of the email
    def mk_outro
        "\n" + ["Jeg håber vi høres ved.", "Håber jeg hører fra jer.", "Vi ses til jobsamtale :)"].sample + "\n"
    end

    ##
    # Generates a random sender line
    def mk_sender
        ["-- ", "Med kærlig hilsen, ", "Med venlig hilsen, ", "MVH, ", "Hilsen "]. sample + "Nikolaj Lepka\n" +
        "Telefon: 25 14 66 83\n" +
        "Email: slench102@gmail.com\n" +
        "Github: https://github.com/ElectricCoffee\n" +
        "Twitter: https://twitter.com/Electric_Coffee\n\n"
    end

    ##
    # Generates the entire email
    def mk_email
        ps = "P.S. Jeg har vedhæftet relevante dokumenter, så som eksamensbevis og CV i mailen."
        ps += "\nP.P.S Denne email var genereret med, og sendt fra et Ruby script :)" if @skills and @skills.include? "Ruby"
        "#{mk_intro}\n#{mk_body}#{mk_outro}#{mk_sender}#{ps}"
    end
end

# set the delivery method to SMTP and load the relevant settings from mailinfo.yml
Mail.defaults do
    delivery_method :smtp, YAML.load_file(MAILINFO)
end

# Load the recipients from yaml
recipients_all = YAML.load_file(RECIPIENTS)

# get only the recipients not contacted
recipients = recipients_all
    .map { |r| Recipient.new r }
    .find_all { |r| r.contacted.nil? }

# add today's date to all the recipients not contacted
recipients_all.each do |r|
    r["contacted"] = Date.today if r["contacted"].nil?
end

# For each recipient that hasn't already been contacted, build and send the email over Google's SMTP server.
for r in recipients do
    puts "Sending mail to #{r.name}"
    mail = Mail.new do
        from "Nikolaj Lepka"
        to r.email
        cc "slench102@gmail.com"
        subject "Datalogikandidat søger job som #{r.position}"
        body r.mk_email

        add_file "#{MAILFILES}/CV.pdf"
        add_file "#{MAILFILES}/karakterark.pdf"
    end

    mail.charset = 'UTF-8' # this doesn't work for some reason...
    mail.deliver
end

# Once everything's done, write the edited yaml file back into recipients.yml
File.open(RECIPIENTS, 'w') do |f|
    f.write(recipients_all.to_yaml)
end