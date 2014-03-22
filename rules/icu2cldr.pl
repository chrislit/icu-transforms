#!/usr/bin/perl

use utf8;
use Encode;
use Unicode::Normalize;

opendir (DIR, ".");
@xlits = grep /\.txt$/, readdir (DIR);

foreach $file (@xlits) {

    open (INF, "<:encoding(utf8)", $file);
    $file =~ s/\.txt$/.xml/;
    $file =~ s/\_/\-/g;
    open (OUTF, ">:encoding(utf8)", "cldr/$file");
    
    print OUTF "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<!DOCTYPE supplementalData SYSTEM \"../../common/dtd/ldmlSupplemental.dtd\">\n<!--\nCopyright © 1991-2013 Unicode, Inc.\nCLDR data files are interpreted according to the LDML specification (http://unicode.org/reports/tr35/)\nFor terms of use, see http://www.unicode.org/copyright.html\n-->\n<supplementalData>\n	<version number=\"\$Revision\$\"/>\n	<generation date=\"\$Date\$\"/>\n	<transforms>\n";

    $file =~ /^(.+?)\-(.+?)(\-(.+?))?\./;
    my $source = $1;
    my $target = $2;
    my $variant = $4;
    
    print OUTF "		<transform source=\"$source\" target=\"$target\" direction=\"both\"";
    print "Creating $source-$target";
    if ($variant ne "") {
	print OUTF " variant=\"$variant\" ";
	print "\/$variant";
    }
    print OUTF ">\n";
    print "\n";

    my $delNextEmpty = 0;

    while (<INF>) {
	my $line = $_;
	$line =~ s/^\x{FEFF}//;
	$line =~ s/[\t\r\n ]*$//;
	$line =~ s/^[\t\r\n ]*//;
	if ($line !~ /^[\t\r\n ]*$/) {

	    $line =~ s/([^\\])<>/$1↔/g;
	    $line =~ s/([^\\])>/$1→/g;
	    $line =~ s/([^\\])</$1←/g;

	    $line =~ s/&/&amp;/g;
	    $line =~ s/</&lt;/g;
	    $line =~ s/>/&gt;/g;

	    $line = NFD($line);

	    if ($line =~ /^\#/) {
		if ($line =~ /^\# \*/) {} #temporary; remove when CLDR data is in good shape
		elsif ($line =~ /^\# (File:|Generated from CLDR)/) {$delNextEmpty = 1}
		elsif ($line =~ /^\#[\s\-]*$/) {} #temporary; remove when CLDR data is in good shape
		else {
		    print OUTF "			<comment>$line<\/comment>\n";
		}
	    }
	    else {
		# Disabling this line; re-enable as necessary;; $line =~ s/\\u([0-9A-Fa-f]{1,6})/chr(hex($1))/eg;
		print OUTF "			<tRule>$line<\/tRule>\n";
	    }
	}
	else {
	    if ($delNextEmpty == 0) {
		print OUTF "\n";
	    }
	    $delNextEmpty = 0;
	}
    }

    print OUTF "		</transform>\n	</transforms>\n</supplementalData>\n";

    close (OUTF);
    close (INF);
}
