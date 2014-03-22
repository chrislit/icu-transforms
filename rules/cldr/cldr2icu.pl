#!/usr/bin/perl

use utf8;
use Encode;
use Unicode::Normalize;

opendir (DIR, ".");
@xlits = grep /\.xml$/, readdir (DIR);

foreach $file (@xlits) {
    open (INF, "<:encoding(UTF-8)", $file);
    $file =~ s/\.xml$/.txt/;
    $file =~ s/\-/\_/g;
    open (OUTF, ">:encoding(UTF-8)", "../$file");

    $file =~ /^(.+?)\_(.+?)(\_(.+?))?\./;
    my $source = $1;
    my $target = $2;
    my $variant = $4;

    print "Creating $source-$target";
    if ($variant ne "") {
	print "\/$variant";
    }
    print "\n";


    print OUTF chr(0xFEFF);

    my $doc = "# ***************************************************************************\n";
    $doc .= "# *\n";
    $doc .= "# *  Copyright (C) 2014\n";
    $doc .= "# *  All Rights Reserved.\n";
    $doc .= "# *\n";
    $doc .= "# ***************************************************************************\n";
    $doc .= "# File: " . $file . "\n";
    $doc .= "# Generated from CLDR\n\n";
    
    while (<INF>) {
	my $line = $_;
	$line =~ s/^\x{FEFF}//;
	$line =~ s/[\t\r\n ]*$//;
	$line =~ s/^[\t\r\n ]*//;
	
	$line =~ s/<[^<>]+?>//g;
	
	if ($line !~ /^[\t\r\n ]*$/) {

	    $line =~ s/↔/<>/g;
	    $line =~ s/→/>/g;
	    $line =~ s/←/</g;

	    $line =~ s/&lt;/>/g;
	    $line =~ s/&gt;/>/g;
	    $line =~ s/&amp;/&/g;

	    #$line =~ s/\\u([0-9A-Fa-f]{1,6})/chr(hex($1))/eg;

	    $line = NFD($line);
	    
	    $doc .= $line . "\n";
	}
	else {
	    $doc .= "\n";
	}
    }

    $doc =~ s/<!--.+?-->[\s]*//s;
    $doc =~ s/\n\n+/\n\n/s;
    $doc =~ s/\s*$//s;
    $doc .= "\n";

    print OUTF "$doc";    
    close (OUTF);
    close (INF);
}
