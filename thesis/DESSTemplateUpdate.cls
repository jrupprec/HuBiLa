%
% LLNCS DOCUMENT CLASS -- version 2.10
% for LaTeX2e
%
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{DESSTemplate}[2012/02/15]

\typeout{***********************************************************************}
\typeout{* Data Science in the Economic and Social Sciences *}
\typeout{***********************************************************************}

\LoadClass[12pt,a4paper,twoside,titlepage,headings=big,chapterprefix=true]{scrbook}
\RequirePackage[twoside,bindingoffset=0.5cm,includeheadfoot,twoside,top=2cm,bottom=2cm,inner=3cm, outer=2.5cm]{geometry} %Page layout

\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[english]{babel}
\RequirePackage[babel]{csquotes}
\RequirePackage[sorting=none, backend=bibtex]{biblatex}
\RequirePackage[colorlinks,hidelinks, pdfpagelabels,pdfstartview = FitH, bookmarksopen = true,bookmarksnumbered = true, linkcolor = black, plainpages = false, hypertexnames = false, citecolor = black]{hyperref}
\usepackage[dvipsnames,table]{xcolor}

%layout packages
\RequirePackage{layout} %print layout options 
\RequirePackage{lmodern} %Change font size of chapter titles
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhead{} % clear all header fields
\fancyhead[RO]{\textsl{\rightmark}}
\fancyhead[LE]{\textsl{\leftmark}}
\fancyfoot{} % clear all footer fields
\fancyfoot[CE,CO]{\thepage}
\fancyfoot[LO,RO]{}
\fancyfoot[LE,RE]{}
\renewcommand{\headrulewidth}{.4pt}
\renewcommand{\footrulewidth}{.4pt}
\RequirePackage[textfont=it]{caption} %add labelfont when other style preferred
\setcapindent{0pt}
%\captionsetup{indention= -2cm} %second line of caption is aligned with leftmost side
%\RequirePackage[font=small,margin=2.5cm,labelfont=bf]{caption}
%\captionsetup[figure]{% use subfigure to confine changes to subcaptions
%  justification = RaggedRight, % Or justified
  %format=hang}

%Necessary Packages
\RequirePackage{mathptmx} %Sets the font of the entire document + math mode to times new roman
\DeclareMathAlphabet{\mathcal}{OMS}{cmsy}{m}{n} %Resets the mathcal font to default
\RequirePackage{ae}
\RequirePackage{amsmath}
\RequirePackage{amsxtra}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage{amsthm}
\RequirePackage{algorithm} %Algorithm environment
\RequirePackage{algpseudocode} %Pseudocode commands used in algorithm
\RequirePackage{breakurl}
\RequirePackage{dsfont}
\RequirePackage{enumerate}
\RequirePackage{enumitem}
\RequirePackage{eurosym}
\RequirePackage{epsfig}
\RequirePackage{float}
\RequirePackage{graphicx}
\RequirePackage{listings}
\RequirePackage{mathtools} %eg coloneqq defined here
\RequirePackage{multicol}
\RequirePackage{setspace}
\RequirePackage{tabularx}
\RequirePackage{textcomp}
\RequirePackage{tikz}
\usetikzlibrary{arrows, backgrounds,calc, decorations.pathreplacing, graphs, graphs.standard, positioning,shapes,shadows, snakes}
\RequirePackage{times}
\RequirePackage{verbatim}
\RequirePackage{wasysym}
\RequirePackage{xkeyval}
\RequirePackage{xargs}  

\rmfamily

\widowpenalty=10000
\clubpenalty=10000

\AtBeginDocument{

\addtokomafont{chapterprefix}{\raggedleft}
\addtokomafont{section}{\huge}
\addtokomafont{subsection}{\Large}
\addtokomafont{subsubsection}{\large}

\renewcommand*{\chapterformat}{%
	\mbox{\scalebox{1.5}{{\nobreakspace}}%
		\scalebox{4}{\color{gray}\thechapter\autodot}\enskip}
	{\par%
		\kern-.75\ht\strutbox\rule{\linewidth}{.8pt}%
	}%	
}
\pagenumbering{Roman} %start with roman literals for counting
}


\renewenvironment{figure}
               {\setcounter{subfigure}{0}
                \@float{figure}}
               {\end@float}
\renewenvironment{table}
               {\setcounter{subtable}{0}
                \@float{table}}
               {\end@float}





\renewcommand{\baselinestretch}{1.2} %Spacing between lines

\renewcommand{\labelitemi}{--}
%\setlength{\parindent}{0cm}


\renewcommand{\algorithmicrequire}{\textbf{Input: }}
\renewcommand{\algorithmicensure}{\textbf{Output: }}

	
\DeclareGraphicsRule{.pdf}{pdf}{.pdf}{}