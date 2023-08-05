(* ::Package:: *)

(* ::Input:: *)
(*BeginPackage["SubSpaces`"];*)
(*Clear["SubSpaces`*"];*)
(*ListSubSpaces::usage="Get a list of all linear independent (sub-)spaces of a lower left triangular matrix.";*)
(*Begin["SubSpaces`Private`"];*)


(* ::Input:: *)
(*SubMatrix[triangular_]:=Module[{sub1=triangular-DiagonalMatrix[Diagonal[triangular]],dim=Dimensions[triangular][[1]]},sub1[[2;;dim,1;;dim-1]]*)
(*]*)
(*SMLowLeftNoDiag[tri_]:=SubMatrix[tri]/;(MatrixQ[tri]&&Dimensions[tri][[1]]>2)*)
(*SMLowLeftNoDiag[tri_]:=False/;(MatrixQ[tri]&&Dimensions[tri][[1]]<=2)*)
(*ListSubSpaces[tri_]:=Module[{sub=tri},NestWhileList[SMLowLeftNoDiag,sub,Dimensions[#][[1]]>2 &]]*)


(* ::Input:: *)
(*End[];*)
(*EndPackage[];*)
