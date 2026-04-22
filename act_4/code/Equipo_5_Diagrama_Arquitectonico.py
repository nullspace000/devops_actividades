# Para regenerar el PDF ejecutar en bash:
# pip install reportlab pypdf
# python aws_pdf.py

import math
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, KeepTogether, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Flowable

W_PAGE, H_PAGE = A4

# ── Palette
C_ORANGE = colors.HexColor("#FF9900")
C_DARK   = colors.HexColor("#232F3E")
C_BLUE   = colors.HexColor("#1A73E8")
C_LIGHT  = colors.HexColor("#EBF5FB")
C_GREEN  = colors.HexColor("#27AE60")
C_RED    = colors.HexColor("#E74C3C")
C_GRAY   = colors.HexColor("#F2F3F4")
C_GOLD   = colors.HexColor("#F39C12")
C_PUB    = colors.HexColor("#D5F5E3")
C_PRIV   = colors.HexColor("#FDEDEC")
C_VPC    = colors.HexColor("#EAF4FB")
C_DARK2  = colors.HexColor("#1B2631")

# ── Header/footer callback
def page_cb(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_DARK)
    canvas.rect(0, H_PAGE - 1.05*cm, W_PAGE, 1.05*cm, fill=1, stroke=0)
    canvas.setFillColor(C_ORANGE)
    canvas.setFont("Helvetica-Bold", 8.5)
    canvas.drawString(1.5*cm, H_PAGE - 0.72*cm,
        "Diagrama Arquitectonico AWS  |  Empresa de Transporte Nacional e Internacional")
    canvas.setFillColor(C_DARK)
    canvas.rect(0, 0, W_PAGE, 0.75*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 0.25*cm, "Actividad 4  |  Arquitectura Cloud AWS")
    canvas.drawRightString(W_PAGE - 1.5*cm, 0.25*cm, f"Pagina {doc.page}")
    canvas.restoreState()

# ── Styles
def get_styles():
    s = {}
    s["h1"] = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=12,
        textColor=colors.white, backColor=C_DARK, borderPad=7,
        leading=17, spaceAfter=7, spaceBefore=10)
    s["h2"] = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5,
        textColor=C_DARK, backColor=C_GRAY, borderPad=5,
        leading=15, spaceAfter=5, spaceBefore=8)
    s["h3"] = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=9.5,
        textColor=C_BLUE, spaceAfter=3, spaceBefore=6)
    s["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=9,
        textColor=C_DARK, alignment=TA_JUSTIFY, leading=13, spaceAfter=4)
    s["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9,
        textColor=C_DARK, leftIndent=14, leading=13, spaceAfter=2)
    s["code"] = ParagraphStyle("code", fontName="Courier", fontSize=7.5,
        textColor=colors.white, backColor=C_DARK, borderPad=6,
        leading=11, spaceAfter=5)
    s["caption"] = ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=7.5,
        textColor=colors.HexColor("#7F8C8D"), alignment=TA_CENTER, spaceAfter=6)
    s["note"] = ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8.5,
        textColor=colors.HexColor("#1A5276"), backColor=colors.HexColor("#D6EAF8"),
        borderPad=6, leading=13, spaceAfter=5)
    return s

S = get_styles()

# ── Shortcuts
def h1(t):  return Paragraph(f"  {t}", S["h1"])
def h2(t):  return Paragraph(f"  {t}", S["h2"])
def h3(t):  return Paragraph(t, S["h3"])
def bd(t):  return Paragraph(t, S["body"])
def bp(t):  return Paragraph(f"&#8226;  {t}", S["bullet"])
def nb(t):  return Paragraph(f"Nota:  {t}", S["note"])
def sp(n=6):return Spacer(1, n)
def hr():   return HRFlowable(width="100%", thickness=0.4,
                               color=colors.HexColor("#BDC3C7"))

def mk_table(data, widths, hbg=C_DARK, alt=C_LIGHT):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0,0), (-1,0), hbg),
        ("TEXTCOLOR",      (0,0), (-1,0), colors.white),
        ("FONTNAME",       (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",       (0,0), (-1,0), 8),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, alt]),
        ("FONTSIZE",       (0,1), (-1,-1), 8),
        ("FONTNAME",       (0,1), (-1,-1), "Helvetica"),
        ("GRID",           (0,0), (-1,-1), 0.4, colors.HexColor("#D5D8DC")),
        ("ALIGN",          (0,0), (-1,-1), "LEFT"),
        ("VALIGN",         (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",     (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
        ("LEFTPADDING",    (0,0), (-1,-1), 6),
    ]))
    return t

# ════════════════════════════════════════════════════════
# COVER
# ════════════════════════════════════════════════════════
class Cover(Flowable):
    def __init__(self): Flowable.__init__(self); self.width=W_PAGE; self.height=H_PAGE
    def wrap(self,aw,ah): return self.width, self.height
    def isIndexing(self): return 0
    def draw(self):
        c = self.canv
        c.setFillColor(C_DARK); c.rect(0,0,W_PAGE,H_PAGE,fill=1,stroke=0)
        c.setFillColor(C_ORANGE)
        c.rect(0, H_PAGE-0.7*cm, W_PAGE, 0.7*cm, fill=1, stroke=0)
        c.rect(0, 0, W_PAGE, 0.7*cm, fill=1, stroke=0)
        # decorative circles
        for cx,cy,r,a in [(W_PAGE*0.83,H_PAGE*0.77,88,0.055),(W_PAGE*0.12,H_PAGE*0.22,62,0.04)]:
            c.saveState(); c.setFillColor(colors.white); c.setFillAlpha(a)
            c.circle(cx,cy,r,fill=1,stroke=0); c.restoreState()
        # AWS badge
        c.setFillColor(C_ORANGE); c.setFont("Helvetica-Bold",46)
        c.drawCentredString(W_PAGE/2, H_PAGE*0.74, "AWS")
        c.setFillColor(colors.white); c.setFont("Helvetica",13)
        c.drawCentredString(W_PAGE/2, H_PAGE*0.69, "Amazon Web Services  |  Cloud Architecture")
        # Title
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",21)
        c.drawCentredString(W_PAGE/2, H_PAGE*0.60, "Diagrama Arquitectonico")
        c.setFillColor(C_ORANGE); c.setFont("Helvetica-Bold",16)
        c.drawCentredString(W_PAGE/2, H_PAGE*0.55, "Solucion Cloud para Empresa de Transporte")
        c.setFillColor(colors.HexColor("#BDC3C7")); c.setFont("Helvetica",12)
        c.drawCentredString(W_PAGE/2, H_PAGE*0.51, "Nacional e Internacional")
        # divider
        c.setStrokeColor(C_ORANGE); c.setLineWidth(1.5)
        c.line(W_PAGE*0.22, H_PAGE*0.48, W_PAGE*0.78, H_PAGE*0.48)
        # info rows
        rows=[
            ("Actividad",  "4  -  Arquitectura en la Nube"),
            ("Region AWS", "us-east-1  (N. Virginia)"),
            ("Servicios",  "VPC  EC2  S3  DynamoDB  RDS  CloudWatch  IAM"),
            ("Patron",     "Multi-tier  |  Alta Disponibilidad  |  99.99% SLA"),
            ("Entregable", "Documento tecnico en formato PDF"),
        ]
        for i,(k,v) in enumerate(rows):
            y = H_PAGE*0.44 - i*0.62*cm
            c.setFillColor(C_ORANGE); c.setFont("Helvetica-Bold",9)
            c.drawString(W_PAGE*0.22, y, k)
            c.setFillColor(colors.white); c.setFont("Helvetica",9)
            c.drawString(W_PAGE*0.39, y, v)
        c.setFillColor(colors.HexColor("#7F8C8D")); c.setFont("Helvetica-Oblique",7.5)
        c.drawCentredString(W_PAGE/2, 1.1*cm,
            "Confidencial  -  Proyecto de Migracion a la Nube")

# ════════════════════════════════════════════════════════
# VPC DIAGRAM
# ════════════════════════════════════════════════════════
class VPCDiagram(Flowable):
    def __init__(self, w=16*cm, h=14*cm):
        Flowable.__init__(self); self.width=w; self.height=h
    def wrap(self,*_): return self.width, self.height

    def draw(self):
        c = self.canv
        W, H = self.width, self.height

        def rr(x,y,w,h,r=4,fc=None,sc=None,lw=1):
            c.saveState()
            if fc: c.setFillColor(fc)
            if sc: c.setStrokeColor(sc); c.setLineWidth(lw)
            c.roundRect(x,y,w,h,r, fill=1 if fc else 0, stroke=1 if sc else 0)
            c.restoreState()

        def txt(text,x,y,sz=7,bold=False,col=C_DARK,align="c"):
            c.saveState(); c.setFillColor(col)
            c.setFont("Helvetica-Bold" if bold else "Helvetica", sz)
            if align=="c": c.drawCentredString(x,y,text)
            else: c.drawString(x,y,text)
            c.restoreState()

        def arrow(x1,y1,x2,y2,col=C_DARK,dash=False):
            c.saveState(); c.setStrokeColor(col); c.setLineWidth(1.1)
            if dash: c.setDash([5,3])
            c.line(x1,y1,x2,y2)
            dx,dy=x2-x1,y2-y1; L=math.sqrt(dx*dx+dy*dy) or 1
            ux,uy=dx/L,dy/L; ax,ay=x2-8*ux,y2-8*uy
            c.setFillColor(col); c.setStrokeColor(col)
            px,py=-uy*3.5,ux*3.5
            p=c.beginPath(); p.moveTo(x2,y2)
            p.lineTo(ax+px,ay+py); p.lineTo(ax-px,ay-py)
            p.close(); c.drawPath(p,fill=1,stroke=0); c.restoreState()

        # VPC outer box
        rr(4,4,W-8,H-8,r=7,fc=C_VPC,sc=C_BLUE,lw=2)
        txt("VPC   10.0.0.0/16   |   Region: us-east-1",W/2,H-14,sz=9,bold=True,col=C_BLUE)

        # Internet box
        rr(W/2-40,H-36,80,20,r=10,fc=colors.HexColor("#D6EAF8"),sc=C_BLUE,lw=1.2)
        txt("Internet  /  Usuarios",W/2,H-23,sz=8,bold=True,col=C_BLUE)

        # IGW
        igw_cx=W/2; igw_y=H-67
        rr(igw_cx-34,igw_y,68,20,r=4,fc=C_ORANGE,sc=colors.HexColor("#D68910"),lw=1.2)
        txt("Internet Gateway (IGW)",igw_cx,igw_y+12,sz=7.5,bold=True,col=colors.white)
        txt("Punto de entrada a la VPC",igw_cx,igw_y+3,sz=6,col=colors.white)
        arrow(W/2,H-36,W/2,igw_y+20,col=C_BLUE)

        # AZ dashed border
        az_x=16; az_y=12; az_w=W-32; az_h=igw_y-22
        c.saveState(); c.setStrokeColor(colors.HexColor("#99A3A4"))
        c.setDash([5,3]); c.setLineWidth(0.8)
        c.rect(az_x,az_y,az_w,az_h,stroke=1,fill=0); c.restoreState()
        txt("Availability Zone  us-east-1a", az_x+az_w/2, az_y+az_h-7,
            sz=6.5, col=colors.HexColor("#7F8C8D"))

        # Public subnet
        pw=(az_w-18)/2; px=az_x+5; py=az_y+13; ph=az_h-22
        rr(px,py,pw,ph,r=5,fc=C_PUB,sc=C_GREEN,lw=1.5)
        txt("Subred Publica",px+pw/2,py+ph-11,sz=8,bold=True,col=C_GREEN)
        txt("10.0.1.0/24",px+pw/2,py+ph-21,sz=7,col=colors.HexColor("#1D8348"))

        # ALB in public
        alb_bx=px+pw/2-36; alb_by=py+ph-54
        rr(alb_bx,alb_by,72,22,r=4,fc=C_BLUE,sc=colors.HexColor("#1565C0"),lw=1)
        txt("App Load Balancer",px+pw/2,alb_by+13,sz=7,bold=True,col=colors.white)
        txt("Puertos 80 / 443",px+pw/2,alb_by+4,sz=6.5,col=colors.white)

        # NAT GW in public
        nat_bx=px+pw/2-32; nat_by=py+8
        rr(nat_bx,nat_by,64,22,r=4,fc=C_GOLD,sc=colors.HexColor("#D68910"),lw=1)
        txt("NAT Gateway",px+pw/2,nat_by+13,sz=7,bold=True,col=colors.white)
        txt("Elastic IP estatica",px+pw/2,nat_by+4,sz=6.5,col=colors.white)

        # Private subnet
        prx=az_x+az_w-pw-5; pry=py; prh=ph
        rr(prx,pry,pw,prh,r=5,fc=C_PRIV,sc=C_RED,lw=1.5)
        txt("Subred Privada",prx+pw/2,pry+prh-11,sz=8,bold=True,col=C_RED)
        txt("10.0.2.0/24",prx+pw/2,pry+prh-21,sz=7,col=colors.HexColor("#B71C1C"))

        # EC2 ERP
        e1x=prx+7; e1y=pry+prh-57
        rr(e1x,e1y,54,34,r=4,fc=colors.HexColor("#FEF9E7"),sc=C_ORANGE)
        txt("EC2",e1x+27,e1y+23,sz=8,bold=True,col=C_ORANGE)
        txt("t3.medium",e1x+27,e1y+13,sz=6.5,col=C_DARK)
        txt("ERP Logistica",e1x+27,e1y+4,sz=6,col=C_DARK)

        # EC2 Flota
        e2x=prx+pw-61; e2y=e1y
        rr(e2x,e2y,54,34,r=4,fc=colors.HexColor("#F0FFF0"),sc=C_GREEN)
        txt("EC2",e2x+27,e2y+23,sz=8,bold=True,col=C_GREEN)
        txt("t3.medium",e2x+27,e2y+13,sz=6.5,col=C_DARK)
        txt("Monit. Flota",e2x+27,e2y+4,sz=6,col=C_DARK)

        # RDS
        rdx=prx+pw/2-36; rdy=pry+7
        rr(rdx,rdy,72,30,r=4,fc=colors.HexColor("#EAF2FF"),sc=C_BLUE)
        txt("Amazon RDS",prx+pw/2,rdy+20,sz=7.5,bold=True,col=C_BLUE)
        txt("SQL Server  Multi-AZ",prx+pw/2,rdy+10,sz=6.5,col=C_DARK)
        txt("Backup 7 dias",prx+pw/2,rdy+2,sz=6,col=C_DARK)

        # Bottom services
        sw=(W-30)/3; sy=5
        svcs=[
            ("S3 Bucket","transporte-logistica-docs",colors.HexColor("#FEF9E7"),C_ORANGE),
            ("DynamoDB","Rutas  y  Clientes NoSQL",colors.HexColor("#EAF2FF"),C_BLUE),
            ("CloudWatch","Metricas  y  Alarmas",colors.HexColor("#FDEDEC"),C_RED),
        ]
        for i,(nm,ds,fc,sc) in enumerate(svcs):
            bx=12+i*(sw+3)
            rr(bx,sy,sw,25,r=4,fc=fc,sc=sc)
            txt(nm,bx+sw/2,sy+15,sz=7.5,bold=True,col=sc)
            txt(ds,bx+sw/2,sy+5,sz=6.5,col=C_DARK)

        # IAM box (small)
        rr(W-72,sy,60,25,r=4,fc=colors.HexColor("#F9F0FF"),sc=colors.HexColor("#8E44AD"))
        txt("IAM + MFA",W-42,sy+15,sz=7.5,bold=True,col=colors.HexColor("#8E44AD"))
        txt("Roles y Politicas",W-42,sy+5,sz=6.5,col=C_DARK)

        # Arrows
        arrow(igw_cx,igw_y,px+pw/2,alb_by+22,col=C_GREEN)
        arrow(px+pw,alb_by+11,e1x,e1y+17,col=C_BLUE,dash=True)
        arrow(px+pw,alb_by+6,e2x,e2y+24,col=C_BLUE,dash=True)
        arrow(e1x+27,e1y,rdx+36,rdy+30,col=C_BLUE,dash=True)
        arrow(px+pw/2,nat_by+22,igw_cx,igw_y,col=C_GOLD,dash=True)
        arrow(e1x+5,e1y+10,px+pw,nat_by+11,col=C_GOLD,dash=True)
        arrow(e1x+27,e1y,12+sw/2,sy+25,col=C_ORANGE,dash=True)
        arrow(e2x+27,e2y,12+sw+3+sw/2,sy+25,col=C_BLUE,dash=True)
        arrow(rdx+36,rdy,12+2*(sw+3)+sw/2,sy+25,col=C_RED,dash=True)

        # Legend
        lx=W-95; ly=H-78
        rr(lx-3,ly-20,92,26,r=3,fc=colors.HexColor("#FDFEFE"),
           sc=colors.HexColor("#BDC3C7"),lw=0.5)
        txt("LEYENDA",lx+43,ly+2,sz=6.5,bold=True,col=C_DARK)
        for i,(col2,label) in enumerate([
            (C_GREEN,"Trafico publico entrante"),
            (C_BLUE,"Trafico interno VPC"),
            (C_GOLD,"Trafico NAT salida"),
        ]):
            ly2=ly-7-i*7
            c.saveState(); c.setStrokeColor(col2); c.setLineWidth(1)
            c.line(lx,ly2,lx+12,ly2); c.restoreState()
            txt(label,lx+14,ly2-2.5,sz=6,col=C_DARK,align="l")

# ════════════════════════════════════════════════════════
# CLOUDWATCH DASHBOARD MOCK
# ════════════════════════════════════════════════════════
class CWDash(Flowable):
    def __init__(self, w=16*cm, h=7.5*cm):
        Flowable.__init__(self); self.width=w; self.height=h
    def wrap(self,*_): return self.width, self.height
    def draw(self):
        c=self.canv; W,H=self.width,self.height
        def rr(x,y,w,h,r=3,fc=None,sc=None,lw=0.8):
            c.saveState()
            if fc: c.setFillColor(fc)
            if sc: c.setStrokeColor(sc); c.setLineWidth(lw)
            c.roundRect(x,y,w,h,r,fill=1 if fc else 0,stroke=1 if sc else 0)
            c.restoreState()
        def txt(t,x,y,sz=7,bold=False,col=C_DARK,align="c"):
            c.saveState(); c.setFillColor(col)
            c.setFont("Helvetica-Bold" if bold else "Helvetica",sz)
            if align=="c": c.drawCentredString(x,y,t)
            else: c.drawString(x,y,t)
            c.restoreState()
        # header bar
        rr(0,H-20,W,20,r=0,fc=C_DARK)
        txt("CloudWatch Dashboard  -  TransporteLogistica  (us-east-1)",
            W/2,H-12,sz=8.5,bold=True,col=C_ORANGE)
        # metric cards
        cards=[
            ("CPU Utilization","68 %","EC2-ERP-Logistica",C_ORANGE,"Normal"),
            ("Network In","1.24 GB/h","EC2-Flota-Monitor",C_BLUE,"Normal"),
            ("DB Connections","47 / 100","RDS SQL Server",C_GREEN,"Normal"),
            ("ALARMA CRITICA","CPU > 80%","UMBRAL SUPERADO",C_RED,"ACTIVA"),
        ]
        cw=(W-14)/4; cy=H-100
        for i,(title,val,sub,col2,status) in enumerate(cards):
            bx=5+i*(cw+3)
            rr(bx,cy,cw,65,r=4,fc=C_DARK2,sc=col2,lw=1.5)
            txt(title,bx+cw/2,cy+55,sz=6.5,bold=True,col=col2)
            txt(val,bx+cw/2,cy+38,sz=12,bold=True,col=colors.white)
            txt(sub,bx+cw/2,cy+25,sz=6,col=colors.HexColor("#AAB7C4"))
            scol=C_GREEN if status=="Normal" else C_RED
            rr(bx+8,cy+8,cw-16,15,r=3,fc=scol)
            txt(status,bx+cw/2,cy+12,sz=6.5,bold=True,col=colors.white)
        # sparkline area
        sp_x=5; sp_y=cy-48; sp_w=W-10; sp_h=38
        rr(sp_x,sp_y,sp_w,sp_h,r=3,fc=C_DARK2,sc=C_BLUE,lw=0.8)
        txt("CPU Utilization  -  EC2-ERP-Logistica  (ultimas 6 horas)",
            sp_x+sp_w/2,sp_y+sp_h-8,sz=7,bold=True,col=C_BLUE)
        # fake graph
        pts=[0.28,0.42,0.38,0.52,0.65,0.48,0.70,0.63,0.55,0.80,0.75,0.68]
        gx0=sp_x+8; gy0=sp_y+5; gw=sp_w-16; gh=sp_h-18
        pw=gw/(len(pts)-1)
        c.saveState(); c.setStrokeColor(C_ORANGE); c.setLineWidth(1.3)
        path=c.beginPath()
        path.moveTo(gx0,gy0+pts[0]*gh)
        for j,v in enumerate(pts[1:],1):
            path.lineTo(gx0+j*pw,gy0+v*gh)
        c.drawPath(path)
        c.setStrokeColor(C_RED); c.setDash([4,2]); c.setLineWidth(1)
        c.line(gx0,gy0+0.80*gh,gx0+gw,gy0+0.80*gh)
        c.restoreState()
        txt("Umbral 80%",gx0+gw+2,gy0+0.80*gh-2,sz=6,bold=True,col=C_RED,align="l")
        # x axis labels
        labels=["09:00","10:00","11:00","12:00","13:00","14:00","15:00",
                "16:00","17:00","18:00","19:00","20:00"]
        for j,lb in enumerate(labels):
            txt(lb,gx0+j*pw,sp_y+2,sz=5.5,col=colors.HexColor("#AAB7C4"))

# ════════════════════════════════════════════════════════
# S3 POLICY BOX
# ════════════════════════════════════════════════════════
class S3Box(Flowable):
    def __init__(self,w=16*cm,h=5.5*cm):
        Flowable.__init__(self); self.width=w; self.height=h
    def wrap(self,*_): return self.width,self.height
    def draw(self):
        c=self.canv; W,H=self.width,self.height
        c.setFillColor(C_DARK); c.rect(0,H-18,W,18,fill=1,stroke=0)
        c.setFillColor(C_ORANGE); c.setFont("Helvetica-Bold",8.5)
        c.drawString(8,H-11,"S3 Bucket Policy  -  transporte-logistica-documentos")
        c.setFillColor(C_GREEN); c.setFont("Helvetica",7)
        c.drawRightString(W-8,H-11,"Acceso publico: BLOQUEADO")
        c.setFillColor(colors.HexColor("#1E2B3C")); c.rect(0,0,W,H-18,fill=1,stroke=0)
        lines=[
            ("{","white"),
            ('  "Version": "2012-10-17",','white'),
            ('  "Statement": [{',"white"),
            ('    "Sid": "AllowEC2RoleOnly",',"#F0E68C"),
            ('    "Effect": "Allow",',"#98FB98"),
            ('    "Principal": {',"white"),
            ('      "AWS": "arn:aws:iam::123456789012:role/EC2-S3-Access-Role"',"#87CEEB"),
            ('    },',"white"),
            ('    "Action": ["s3:GetObject","s3:PutObject","s3:DeleteObject"],',"#FFB6C1"),
            ('    "Resource": "arn:aws:s3:::transporte-logistica-documentos/*"',"#87CEEB"),
            ('  }]',"white"),
            ("}",'white'),
        ]
        for i,(line,col) in enumerate(lines):
            c.setFillColor(colors.HexColor(col) if col!="white" else colors.white)
            c.setFont("Courier",7.2)
            y=H-22-i*9.8
            if y>2: c.drawString(8,y,line)

# ════════════════════════════════════════════════════════
# DYNAMODB TABLE MOCK
# ════════════════════════════════════════════════════════
class DynaBox(Flowable):
    def __init__(self,w=16*cm,h=4*cm):
        Flowable.__init__(self); self.width=w; self.height=h
    def wrap(self,*_): return self.width,self.height
    def draw(self):
        c=self.canv; W,H=self.width,self.height
        c.setFillColor(C_BLUE); c.roundRect(0,H-18,W,18,3,fill=1,stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8.5)
        c.drawString(8,H-11,
            "DynamoDB  -  Tabla: RutasTransporte  |  On-Demand  |  GSI: estado-index")
        cols=["rutaId (PK)","conductorId (SK)","origen","destino",
              "estado","fechaEstimada","carga_kg"]
        cw=W/len(cols)
        rows=[
            ["RUT-0042","COND-019","CDMX","MTY","En ruta","2025-08-14","12,500"],
            ["RUT-0043","COND-007","GDL","TIJ","Pendiente","2025-08-15","8,200"],
            ["RUT-0044","COND-031","MTY","CDMX","Entregado","2025-08-13","15,000"],
        ]
        rh=(H-18)/4
        for j,col in enumerate(cols):
            bx=j*cw
            c.setFillColor(colors.HexColor("#1A5276"))
            c.rect(bx,H-18-rh,cw,rh,fill=1,stroke=0)
            c.setStrokeColor(colors.HexColor("#5DADE2")); c.setLineWidth(0.3)
            c.rect(bx,H-18-rh,cw,rh,fill=0,stroke=1)
            c.setFillColor(colors.HexColor("#AED6F1"))
            c.setFont("Helvetica-Bold",6)
            c.drawCentredString(bx+cw/2,H-18-rh+rh/2-3,col)
        for i,row in enumerate(rows):
            alt=i%2==0
            for j,val in enumerate(row):
                bx=j*cw; by=H-18-(i+2)*rh
                if by<0: break
                c.setFillColor(colors.HexColor("#1B2631") if alt else colors.HexColor("#212F3D"))
                c.rect(bx,by,cw,rh,fill=1,stroke=0)
                c.setStrokeColor(colors.HexColor("#2C3E50")); c.setLineWidth(0.3)
                c.rect(bx,by,cw,rh,fill=0,stroke=1)
                tc=colors.HexColor("#F0E68C") if j==0 else (
                   colors.HexColor("#87CEEB") if j==1 else colors.white)
                c.setFillColor(tc); c.setFont("Helvetica",6.2)
                c.drawCentredString(bx+cw/2,by+rh/2-3,val)

# ════════════════════════════════════════════════════════
# CONSOLE MOCKUP (EC2 launch)
# ════════════════════════════════════════════════════════
class ConsoleMock(Flowable):
    def __init__(self,w=16*cm,h=5.5*cm):
        Flowable.__init__(self); self.width=w; self.height=h
    def wrap(self,*_): return self.width,self.height
    def draw(self):
        c=self.canv; W,H=self.width,self.height
        # window chrome
        c.setFillColor(colors.HexColor("#3C3C3C")); c.roundRect(0,H-18,W,18,3,fill=1,stroke=0)
        for cx,col in [(12,colors.HexColor("#FF5F57")),(24,colors.HexColor("#FEBC2E")),
                       (36,colors.HexColor("#28C840"))]:
            c.setFillColor(col); c.circle(cx,H-9,4,fill=1,stroke=0)
        c.setFillColor(colors.HexColor("#AAB7C4")); c.setFont("Helvetica",7.5)
        c.drawCentredString(W/2,H-12,"AWS Console  -  EC2 > Launch Instance > ERP-Logistica")
        # content area
        c.setFillColor(colors.HexColor("#1E2B3C")); c.rect(0,0,W,H-18,fill=1,stroke=0)
        params=[
            ("AMI","Amazon Linux 2023  (ami-0c02fb55956c7d316)","#AED6F1"),
            ("Tipo","t3.medium  -  2 vCPU  4 GB RAM  5 Gbps red","#F0E68C"),
            ("VPC","TransporteVPC  (10.0.0.0/16)","white"),
            ("Subnet","Privada-1a  (10.0.2.0/24)","white"),
            ("IP Publica","Deshabilitada  (acceso via ALB/VPN)","#FFB6C1"),
            ("Security Group","SG-EC2-ERP  |  puerto 8080 desde ALB, 22 desde VPN","white"),
            ("Rol IAM","EC2-S3-Access-Role","#98FB98"),
            ("Volumen EBS","gp3  50 GB  3000 IOPS  125 MB/s","white"),
        ]
        row_h=(H-20)/len(params)
        for i,(k,v,vc) in enumerate(params):
            y=H-20-(i+1)*row_h+2
            if y<1: break
            alt=i%2==0
            c.setFillColor(colors.HexColor("#243342") if alt else colors.HexColor("#1E2B3C"))
            c.rect(0,y,W,row_h,fill=1,stroke=0)
            c.setFillColor(colors.HexColor("#7F8C8D")); c.setFont("Helvetica-Bold",7)
            c.drawString(6,y+row_h/2-2,k)
            c.setFillColor(colors.HexColor(vc) if vc!="white" else colors.white)
            c.setFont("Courier",7)
            c.drawString(85,y+row_h/2-2,v)

# ════════════════════════════════════════════════════════
# BUILD THE DOCUMENT
# ════════════════════════════════════════════════════════
def build():
    import io
    from reportlab.pdfgen import canvas as pdfcanvas
    from pypdf import PdfWriter, PdfReader

    # ── Cover page (standalone canvas)
    cover_buf = io.BytesIO()
    cv = pdfcanvas.Canvas(cover_buf, pagesize=A4)
    Cover().canv = cv
    # Draw cover manually
    c = cv
    c.setFillColor(C_DARK); c.rect(0,0,W_PAGE,H_PAGE,fill=1,stroke=0)
    c.setFillColor(C_ORANGE)
    c.rect(0,H_PAGE-0.7*cm,W_PAGE,0.7*cm,fill=1,stroke=0)
    c.rect(0,0,W_PAGE,0.7*cm,fill=1,stroke=0)
    for cx2,cy2,r,a in [(W_PAGE*0.83,H_PAGE*0.77,88,0.055),(W_PAGE*0.12,H_PAGE*0.22,62,0.04)]:
        c.saveState(); c.setFillColor(colors.white); c.setFillAlpha(a)
        c.circle(cx2,cy2,r,fill=1,stroke=0); c.restoreState()
    c.setFillColor(C_ORANGE); c.setFont("Helvetica-Bold",46)
    c.drawCentredString(W_PAGE/2,H_PAGE*0.74,"AWS")
    c.setFillColor(colors.white); c.setFont("Helvetica",13)
    c.drawCentredString(W_PAGE/2,H_PAGE*0.69,"Amazon Web Services  |  Cloud Architecture")
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold",21)
    c.drawCentredString(W_PAGE/2,H_PAGE*0.60,"Diagrama Arquitectonico")
    c.setFillColor(C_ORANGE); c.setFont("Helvetica-Bold",16)
    c.drawCentredString(W_PAGE/2,H_PAGE*0.55,"Solucion Cloud para Empresa de Transporte")
    c.setFillColor(colors.HexColor("#BDC3C7")); c.setFont("Helvetica",12)
    c.drawCentredString(W_PAGE/2,H_PAGE*0.51,"Nacional e Internacional")
    c.setStrokeColor(C_ORANGE); c.setLineWidth(1.5)
    c.line(W_PAGE*0.22,H_PAGE*0.48,W_PAGE*0.78,H_PAGE*0.48)
    rows=[("Actividad","4  -  Arquitectura en la Nube"),
          ("Region AWS","us-east-1  (N. Virginia)"),
          ("Servicios","VPC  EC2  S3  DynamoDB  RDS  CloudWatch  IAM"),
          ("Patron","Multi-tier  |  Alta Disponibilidad  |  99.99%% SLA"),
          ("Entregable","Documento tecnico en formato PDF")]
    for i,(k,v) in enumerate(rows):
        y=H_PAGE*0.44-i*0.62*cm
        c.setFillColor(C_ORANGE); c.setFont("Helvetica-Bold",9)
        c.drawString(W_PAGE*0.22,y,k)
        c.setFillColor(colors.white); c.setFont("Helvetica",9)
        c.drawString(W_PAGE*0.39,y,v)
    c.setFillColor(colors.HexColor("#7F8C8D")); c.setFont("Helvetica-Oblique",7.5)
    c.drawCentredString(W_PAGE/2,1.1*cm,"Confidencial  -  Proyecto de Migracion a la Nube")
    c.save()
    cover_buf.seek(0)

    # ── Body pages
    body_buf = io.BytesIO()
    doc = SimpleDocTemplate(body_buf, pagesize=A4,
        leftMargin=1.7*cm, rightMargin=1.7*cm,
        topMargin=1.4*cm, bottomMargin=1.2*cm)
    story = []

    # ── TABLE OF CONTENTS
    story.append(h1("Tabla de Contenido"))
    toc = [
        ["#", "Seccion", "Temas Principales"],
        ["A", "Diseno de Redes  -  VPC",
         "Subnets pub/priv, Internet GW, NAT GW, Security Groups"],
        ["B", "Instancias EC2",
         "Tipos de instancias, configuracion, EBS, AMI, lanzamiento"],
        ["C", "Gestion de Datos",
         "S3 Bucket, politicas IAM, DynamoDB, RDS SQL Server"],
        ["D", "Seguridad y Monitoreo",
         "IAM roles, MFA, CloudWatch, alarmas, CloudTrail"],
        ["-", "Resumen Ejecutivo",
         "Comparativa on-premise vs cloud, KPIs y proximos pasos"],
    ]
    story.append(mk_table(toc, [1*cm, 5*cm, 10.2*cm]))
    story.append(sp(8))
    story.append(nb(
        "Este documento presenta la arquitectura de nube propuesta en AWS para la migracion "
        "de la infraestructura on-premise de una empresa de transporte, abarcando redes, "
        "computo, almacenamiento, bases de datos, seguridad y monitoreo continuo."))
    story.append(PageBreak())

    # ══════════════════════════════════
    # A. VPC
    # ══════════════════════════════════
    story.append(h1("A.  Diseno de Redes en AWS  -  VPC (Virtual Private Cloud)"))
    story.append(bd(
        "Una VPC (Virtual Private Cloud) es una red virtual privada logicamente aislada "
        "dentro de la infraestructura de AWS. Para la empresa de transporte se crea una "
        "VPC con CIDR 10.0.0.0/16 en la region us-east-1 (N. Virginia), proporcionando "
        "hasta 65,534 direcciones IP y control total sobre el enrutamiento, segmentacion "
        "y acceso a la red. Esta VPC reemplaza el switch de capa 3 y el firewall fisico "
        "que la empresa opera actualmente en sus oficinas corporativas."))
    story.append(sp(6))

    story.append(h2("A.1  Diagrama de Arquitectura VPC"))
    story.append(VPCDiagram())
    story.append(Paragraph(
        "Figura 1. Arquitectura VPC completa con subnets publica y privada, Internet Gateway, "
        "NAT Gateway, ALB, instancias EC2, RDS y servicios administrados AWS.",
        S["caption"]))
    story.append(sp(8))

    story.append(h2("A.2  Subnets Publicas y Privadas  -  Diferencias y Casos de Uso"))
    story.append(bd(
        "La segmentacion en subnets es el fundamento de la seguridad perimetral en la VPC. "
        "La arquitectura define dos tipos de subnets con roles distintos y complementarios:"))
    story.append(sp(4))
    sub_data = [
        ["Caracteristica", "Subred Publica  10.0.1.0/24", "Subred Privada  10.0.2.0/24"],
        ["Acceso desde internet", "Si  (via Internet Gateway)", "No  (solo trafico saliente via NAT)"],
        ["Recursos alojados", "ALB, NAT Gateway, Bastion Host", "EC2 ERP, EC2 Flota, Amazon RDS"],
        ["Tabla de rutas", "0.0.0.0/0  ->  igw-xxxxxxxx", "0.0.0.0/0  ->  nat-xxxxxxxx"],
        ["IP publica auto-asignada", "Si (IP dinamica o EIP)", "No (solo IP privada RFC 1918)"],
        ["Nivel de exposicion", "Media  (controlado por SG)", "Minima  (sin ruta directa a internet)"],
        ["Seguridad requerida", "Security Group restrictivo", "SG + Network ACL + sin IP publica"],
        ["Caso de uso transporte", "Balanceador ALB para ERP web", "ERP de logistica, datos de rutas y flota"],
    ]
    story.append(mk_table(sub_data, [4.2*cm, 5.8*cm, 6.2*cm]))
    story.append(sp(8))

    story.append(h2("A.3  Internet Gateway  -  Configuracion y Funcionamiento"))
    story.append(bd(
        "El Internet Gateway (IGW) es un componente redundante, escalable y de alta disponibilidad "
        "que AWS gestiona automaticamente. Permite la comunicacion bidireccional entre la VPC y "
        "la red publica de internet. Es el punto de entrada oficial para los usuarios que acceden "
        "al sistema ERP de la empresa de transporte desde sucursales, clientes o colaboradores externos."))
    story.append(sp(4))
    for step in [
        "Crear IGW: AWS Console > VPC > Internet Gateways > Create Internet Gateway > Nombre: TransporteIGW.",
        "Adjuntar a la VPC: seleccionar TransporteIGW > Actions > Attach to VPC > TransporteVPC.",
        "Actualizar tabla de rutas de la subnet publica: agregar regla Destino 0.0.0.0/0, Target: igw-id.",
        "El ALB en la subnet publica recibe el trafico externo y lo distribuye a las instancias EC2 privadas.",
        "Los Security Groups del ALB permiten solo trafico HTTP (80) y HTTPS (443) desde cualquier origen.",
    ]:
        story.append(bp(step))
    story.append(sp(6))

    story.append(h2("A.4  NAT Gateway  -  Salida Segura para Instancias Privadas"))
    story.append(bd(
        "El NAT Gateway permite que las instancias en la subnet PRIVADA inicien conexiones salientes "
        "hacia internet (actualizaciones de sistema operativo, descarga de librerias, llamadas a APIs "
        "externas de logistica) sin estar directamente expuestas al trafico entrante no solicitado. "
        "Se ubica en la subnet publica y tiene asignada una Elastic IP fija para identificacion."))
    story.append(sp(4))
    for step in [
        "Crear en la subnet PUBLICA: VPC > NAT Gateways > Create NAT Gateway > Subnet: Publica-1a.",
        "Asignar Elastic IP (EIP): Click en Allocate Elastic IP > confirmar asignacion.",
        "Actualizar tabla de rutas de la subnet PRIVADA: agregar 0.0.0.0/0 -> nat-gateway-id.",
        "Las instancias EC2 privadas ya pueden ejecutar: yum update, pip install, curl a APIs externas.",
        "El trafico de retorno llega a la EIP del NAT y es redirigido internamente a la instancia correcta.",
    ]:
        story.append(bp(step))
    story.append(sp(6))

    story.append(h2("A.5  Security Groups  -  Firewall Virtual"))
    sg_data = [
        ["Security Group", "Direccion", "Protocolo/Puerto", "Origen / Destino", "Proposito"],
        ["SG-ALB", "Entrada", "TCP 80 (HTTP)", "0.0.0.0/0", "Trafico web publico"],
        ["SG-ALB", "Entrada", "TCP 443 (HTTPS)", "0.0.0.0/0", "Trafico web seguro TLS"],
        ["SG-EC2-ERP", "Entrada", "TCP 8080", "SG-ALB", "Solo desde el balanceador"],
        ["SG-EC2-ERP", "Entrada", "TCP 22 (SSH)", "10.0.0.0/8 via VPN", "Admin solo desde VPN"],
        ["SG-RDS", "Entrada", "TCP 1433 (SQL)", "SG-EC2-ERP", "Solo desde instancias EC2"],
        ["SG-EC2-ERP", "Salida", "All traffic", "0.0.0.0/0 via NAT", "Actualizaciones y APIs"],
    ]
    story.append(mk_table(sg_data, [2.8*cm, 1.8*cm, 2.8*cm, 3.8*cm, 5*cm]))
    story.append(PageBreak())

    # ══════════════════════════════════
    # B. EC2
    # ══════════════════════════════════
    story.append(h1("B.  Instancias Amazon EC2  -  Implementacion por Necesidad"))
    story.append(bd(
        "Amazon EC2 (Elastic Compute Cloud) virtualiza los tres servidores Dell PowerEdge "
        "actuales como instancias en la nube. Cada carga de trabajo recibe el tipo de "
        "instancia mas adecuado a sus requisitos de CPU, memoria, red y almacenamiento, "
        "con la ventaja del escalado automatico y el modelo de pago por uso."))
    story.append(sp(6))

    story.append(h2("B.1  Familias de Instancias AWS  -  Comparativa"))
    inst_data = [
        ["Familia", "Ejemplo", "vCPU", "RAM", "Mejor Para", "Costo aprox/mes"],
        ["Proposito General", "t3.medium", "2", "4 GB",
         "ERP, apps web, microservicios", "~$30 USD"],
        ["Proposito General", "t3.large", "2", "8 GB",
         "Monitoreo de flota, apps medianas", "~$60 USD"],
        ["Opt. Computo", "c6i.xlarge", "4", "8 GB",
         "Procesamiento de rutas, batch", "~$122 USD"],
        ["Opt. Memoria", "r6i.large", "2", "16 GB",
         "Cache, BD en memoria, reportes", "~$95 USD"],
        ["Opt. Almacenamiento", "i4i.large", "2", "16 GB",
         "Logs masivos, analytics rapido", "~$132 USD"],
        ["GPU Compute", "g4dn.xlarge", "4", "16 GB",
         "Vision IA para camiones/video", "~$380 USD"],
    ]
    story.append(mk_table(inst_data,
        [3.2*cm, 2.5*cm, 1.4*cm, 1.5*cm, 5.2*cm, 2.4*cm]))
    story.append(sp(6))

    story.append(h2("B.2  Instancias Recomendadas para la Empresa de Transporte"))
    rec_data = [
        ["Servidor a Migrar", "Instancia AWS", "AMI", "Almacen.", "Justificacion"],
        ["ERP de Logistica", "t3.medium", "Amazon Linux 2023", "gp3 50 GB",
         "Equilibrio costo-rendimiento para app Java/Python con carga moderada"],
        ["Monitoreo de Flota", "t3.medium", "Amazon Linux 2023", "gp3 30 GB",
         "Carga media, CPU burstable ideal para picos de telemetria GPS"],
        ["Servidor de Archivos", "S3 + EFS", "N/A", "S3 ilimitado",
         "Sustituye NAS 12TB, escala sin limite, sin mantenimiento fisico"],
        ["Base de Datos SQL", "RDS db.m6i.large", "SQL Server SE 2019", "gp3 200 GB",
         "Servicio administrado, backups automaticos, failover Multi-AZ"],
    ]
    story.append(mk_table(rec_data,
        [3.0*cm, 2.6*cm, 2.4*cm, 2.2*cm, 5.8*cm]))
    story.append(sp(8))

    story.append(h2("B.3  Configuracion de Lanzamiento EC2  -  Simulacion Consola AWS"))
    story.append(bd(
        "La siguiente simulacion muestra los parametros configurados al lanzar "
        "la instancia del servidor ERP de logistica desde la consola de AWS:"))
    story.append(sp(5))
    story.append(ConsoleMock())
    story.append(Paragraph(
        "Figura 2. Simulacion de la consola AWS al configurar la instancia EC2 "
        "t3.medium para el servidor ERP de logistica en la subnet privada.",
        S["caption"]))
    story.append(PageBreak())

    # ══════════════════════════════════
    # C. DATOS
    # ══════════════════════════════════
    story.append(h1("C.  Gestion de Datos en AWS"))
    story.append(bd(
        "La estrategia de datos en la nube reemplaza la NAS de 12 TB y la instancia local "
        "de SQL Server con servicios administrados de AWS. Se eliminan los respaldos manuales, "
        "se automatizan los snapshots y se garantiza la durabilidad del 99.999999999%% (11 nueves)."))
    story.append(sp(6))

    story.append(h2("C.1  Amazon S3  -  Almacenamiento de Objetos"))
    story.append(bd(
        "Amazon S3 sustituye directamente al servidor de archivos (NAS 12 TB). El bucket "
        "transporte-logistica-documentos almacenara documentos de importacion/exportacion, "
        "manifiestos de carga, facturas, contratos y respaldos de configuracion. "
        "S3 escala automaticamente sin necesidad de aprovisionar capacidad anticipada."))
    story.append(sp(4))
    s3_data = [
        ["Parametro S3", "Valor Configurado", "Beneficio Operativo"],
        ["Nombre del bucket", "transporte-logistica-documentos",
         "Identificador unico global para la empresa"],
        ["Region", "us-east-1 (N. Virginia)",
         "Misma region que la VPC  menor latencia"],
        ["Bloqueo acceso publico", "HABILITADO  (todas las opciones)",
         "Sin URLs publicas  acceso solo via IAM y roles"],
        ["Versionado", "Habilitado",
         "Recupera versiones anteriores de documentos ante error humano"],
        ["Cifrado en reposo", "SSE-S3  (AES-256)",
         "Cifrado automatico sin costo adicional"],
        ["Ciclo de vida", "30d Standard > 90d IA > 365d Glacier",
         "Reduce costos hasta 90%% en archivos historicos"],
        ["Replicacion CRR", "Replica a us-west-2 (Oregon)",
         "Recuperacion ante desastre en otra region AWS"],
        ["Registro de accesos", "Server Access Logging habilitado",
         "Auditoria completa de quien accede a cada documento"],
    ]
    story.append(mk_table(s3_data, [3.8*cm, 4.5*cm, 7.7*cm]))
    story.append(sp(7))

    story.append(h2("C.2  S3 Bucket Policy  -  Control de Acceso IAM"))
    story.append(bd(
        "La politica del bucket restringe el acceso UNICAMENTE al Rol IAM asignado a las "
        "instancias EC2 que procesan documentos de embarque. Ningun usuario humano puede "
        "acceder directamente; solo la aplicacion ERP lo hace de forma programatica "
        "a traves de su rol, siguiendo el principio de minimo privilegio:"))
    story.append(sp(4))
    story.append(S3Box())
    story.append(Paragraph(
        "Figura 3. Bucket Policy de S3 que restringe el acceso exclusivamente al Rol IAM "
        "de la instancia EC2. Acceso publico completamente bloqueado.",
        S["caption"]))
    story.append(sp(8))

    story.append(h2("C.3  Amazon DynamoDB  -  Base de Datos NoSQL"))
    story.append(bd(
        "DynamoDB es la base de datos NoSQL totalmente administrada de AWS. Se utiliza para "
        "datos de alta velocidad de lectura/escritura: estado en tiempo real de rutas activas, "
        "telemetria GPS de la flota y eventos de sensores de los camiones. "
        "A diferencia de SQL Server (relacional con esquema fijo), DynamoDB opera sin esquema "
        "predefinido y escala automaticamente ante cualquier volumen de transacciones."))
    story.append(sp(4))
    comp_data = [
        ["Aspecto", "SQL Server  (Amazon RDS)", "DynamoDB  (NoSQL)"],
        ["Modelo de datos", "Tablas relacionales con esquema", "Clave-valor y documentos JSON"],
        ["Escalado", "Vertical  (instancia mas grande)", "Horizontal automatico ilimitado"],
        ["Latencia", "Milisegundos (variable por consulta)", "< 10 ms constante en cualquier escala"],
        ["Transacciones", "ACID completo  (multi-tabla)", "ACID limitado  (operacion individual)"],
        ["Esquema", "Rigido  (requiere migracion DDL)", "Flexible  (sin ALTER TABLE)"],
        ["Costo", "Por hora de instancia RDS", "Pay-per-request  (por lectura/escritura)"],
        ["Caso de uso", "Inventario, clientes, rutas historicas", "Estado GPS en tiempo real, eventos IoT"],
    ]
    story.append(mk_table(comp_data, [3.5*cm, 5.5*cm, 7.2*cm]))
    story.append(sp(6))

    story.append(h3("Configuracion de la tabla RutasTransporte:"))
    for cfg in [
        "Partition Key: rutaId (String)  -  Identificador unico de cada ruta activa.",
        "Sort Key: conductorId (String)  -  Permite consultas compuestas por conductor.",
        "Capacity Mode: On-Demand  -  AWS escala automaticamente sin configuracion previa.",
        "TTL: fechaExpiracion  -  Elimina registros de rutas completadas despues de 90 dias.",
        "GSI: estado-index  -  Indice secundario para consultar rutas por estado rapidamente.",
        "Streams: habilitados  -  Permite disparar Lambda ante cambios de estado de ruta.",
    ]:
        story.append(bp(cfg))
    story.append(sp(5))
    story.append(DynaBox())
    story.append(Paragraph(
        "Figura 4. Registros de la tabla RutasTransporte en DynamoDB con partition key, "
        "sort key, atributos de estado, fechas y peso de carga.",
        S["caption"]))
    story.append(sp(8))

    story.append(h2("C.4  Amazon RDS  -  Migracion de SQL Server"))
    story.append(bd(
        "La instancia SQL Server on-premise migra a Amazon RDS con AWS Database Migration "
        "Service (DMS), logrando downtime casi nulo al replicar datos en tiempo real "
        "antes del cutover final. RDS elimina parches manuales del SO, backups manuales "
        "y la gestion de alta disponibilidad."))
    rds_data = [
        ["Parametro", "Valor", "Ventaja vs On-Premise"],
        ["Motor", "SQL Server SE 2019", "100%% compatible con esquemas existentes"],
        ["Instancia", "db.m6i.large  2vCPU 8GB", "Rendimiento equivalente al servidor local"],
        ["Almacenamiento", "gp3  200 GB  auto-scaling", "Crece automaticamente sin intervencion"],
        ["Multi-AZ", "Habilitado", "Failover automatico en menos de 2 minutos"],
        ["Backup automatico", "7 dias de retencion", "Restauracion a cualquier punto del tiempo (PITR)"],
        ["Cifrado KMS", "AWS KMS  (AES-256)", "Datos en reposo cifrados, clave gestionada por AWS"],
        ["Monitoreo", "Enhanced Monitoring + CW", "CPU, RAM, IOPS, conexiones en tiempo real"],
        ["Migracion", "AWS DMS  (replicacion live)", "Downtime < 5 minutos en el cutover final"],
    ]
    story.append(mk_table(rds_data, [3.2*cm, 3.8*cm, 9.2*cm]))
    story.append(PageBreak())

    # ══════════════════════════════════
    # D. SEGURIDAD Y MONITOREO
    # ══════════════════════════════════
    story.append(h1("D.  Seguridad y Monitoreo en AWS"))
    story.append(bd(
        "La seguridad sigue el modelo de Responsabilidad Compartida de AWS: AWS protege "
        "la infraestructura fisica, el hypervisor y la red global; la empresa es responsable "
        "de la configuracion logica (IAM, cifrado, Security Groups, parches del SO en EC2). "
        "El monitoreo con CloudWatch garantiza la disponibilidad objetivo del 99.99%%  y "
        "permite reaccionar proactivamente ante incidentes antes de que afecten operaciones."))
    story.append(sp(6))

    story.append(h2("D.1  AWS IAM  -  Identidades, Roles y Politicas"))
    iam_data = [
        ["Entidad IAM", "Tipo", "Politica Aplicada", "Funcion en la Arquitectura"],
        ["admin-ti-001", "Usuario + MFA", "PowerUserAccess", "Admin TI principal, consola AWS"],
        ["admin-ti-002", "Usuario + MFA", "PowerUserAccess", "Admin TI secundario, contingencia"],
        ["EC2-S3-Access-Role", "Rol  (adjunto a EC2)", "S3 bucket especifico", "EC2 escribe documentos en S3 sin access key"],
        ["EC2-CW-Role", "Rol  (adjunto a EC2)", "CloudWatchAgentServer", "EC2 envia metricas custom a CloudWatch"],
        ["RDS-Backup-Role", "Rol  (adjunto a RDS)", "RDS Backup limitado", "RDS ejecuta snapshots automaticos diarios"],
        ["Auditoria-ReadOnly", "Grupo de usuarios", "ReadOnlyAccess", "Equipo de auditoria, sin permisos de cambio"],
    ]
    story.append(mk_table(iam_data, [2.8*cm, 2.5*cm, 3.2*cm, 7.7*cm]))
    story.append(sp(5))
    story.append(nb(
        "Buenas practicas aplicadas: (1) Cuenta root NUNCA usada para operaciones diarias. "
        "(2) MFA obligatorio en todos los usuarios con permisos de escritura o Admin. "
        "(3) Roles IAM en EC2 en lugar de access keys hardcodeadas en el codigo. "
        "(4) Principio de minimo privilegio: cada entidad tiene solo lo que necesita."))
    story.append(sp(8))

    story.append(h2("D.2  Amazon CloudWatch  -  Monitoreo en Tiempo Real"))
    story.append(bd(
        "CloudWatch centraliza el monitoreo de toda la infraestructura: metricas de EC2, "
        "RDS, S3, NAT Gateway, ALB y logs de aplicacion. Para la empresa de transporte "
        "se configura un dashboard unificado que el equipo de TI consulta en tiempo real "
        "y que dispara alertas automaticas antes de que un problema afecte la operacion logistica."))
    story.append(sp(5))
    story.append(CWDash())
    story.append(Paragraph(
        "Figura 5. Dashboard CloudWatch con metricas en tiempo real de CPU, red, conexiones "
        "RDS y alarma critica de umbral de CPU al 80%% con notificacion SNS automatica.",
        S["caption"]))
    story.append(sp(8))

    story.append(h2("D.3  Alarmas CloudWatch Configuradas"))
    alm_data = [
        ["Nombre Alarma", "Metrica", "Umbral", "Accion SNS", "Severidad"],
        ["CPU-ERP-Critica", "CPUUtilization EC2-ERP", "> 80%% x 5min",
         "Email equipo TI", "CRITICA"],
        ["CPU-Flota-Alta", "CPUUtilization EC2-Flota", "> 75%% x 5min",
         "Email + SMS", "ALTA"],
        ["RDS-Conexiones", "DatabaseConnections", "> 80 conex.",
         "Email DBA", "ALTA"],
        ["RDS-Storage", "FreeStorageSpace", "< 20 GB",
         "Email + auto-scale", "CRITICA"],
        ["S3-Errores", "4xxErrors S3", "> 50/minuto",
         "Email seguridad", "MEDIA"],
        ["EC2-StatusFail", "StatusCheckFailed", "= 1 (fallo)",
         "Auto Recovery EC2", "CRITICA"],
        ["NAT-Trafico", "BytesOutToDestination", "> 5 GB/hora",
         "Email (posible exfil)", "ALTA"],
    ]
    story.append(mk_table(alm_data,
        [3.5*cm, 3.4*cm, 2.5*cm, 3.5*cm, 2.0*cm]))
    story.append(sp(7))

    story.append(h2("D.4  Configuracion Paso a Paso: Alarma CPU al 80%%"))
    story.append(bd(
        "Ejemplo practico de como crear la alarma critica de CPU desde la consola de AWS:"))
    story.append(sp(3))
    for step in [
        "Ir a: CloudWatch > Alarms > All Alarms > Create Alarm.",
        "Select metric > EC2 > Per-Instance Metrics > CPUUtilization.",
        "Seleccionar instancia: EC2-ERP-Logistica (i-0a1b2c3d4e5f6g7h8).",
        "Condicion: Greater than  80  durante  1 periodo de 5 minutos.",
        "Accion en estado ALARM: enviar a topico SNS > arn:aws:sns:us-east-1:123456:alertas-ti.",
        "El topico SNS dispara email a ti-equipo@transporte.com.mx y SMS al telefono on-call.",
        "Nombre de alarma: CRITICA-CPU-ERP-Logistica-80pct.",
        "Descripcion: Si persiste >15 min, escalar instancia a t3.large via AWS Auto Scaling.",
    ]:
        story.append(bp(step))
    story.append(sp(7))

    story.append(h2("D.5  AWS CloudTrail  -  Auditoria de Acciones"))
    story.append(bd(
        "CloudTrail registra CADA accion realizada en la cuenta AWS: quien creo una instancia, "
        "quien modifico una politica IAM, quien borro un objeto de S3. Para la empresa de "
        "transporte esto es critico para cumplir con regulaciones aduaneras y de auditoria "
        "de operaciones internacionales."))
    trail_data = [
        ["Configuracion", "Valor", "Proposito"],
        ["Trail name", "TransporteLogistica-Trail", "Identificador del trail en us-east-1"],
        ["Multi-region", "Habilitado", "Captura eventos en todas las regiones"],
        ["S3 destino logs", "bucket-cloudtrail-transporte", "Almacena logs cifrados 90 dias"],
        ["CloudWatch Logs", "Integrado", "Alertas en tiempo real ante acciones sospechosas"],
        ["Event selectors", "Management + Data events", "Incluye acciones en S3 y DynamoDB"],
        ["Log file validation", "Habilitado", "Detecta modificacion o eliminacion de logs"],
    ]
    story.append(mk_table(trail_data, [4*cm, 4.5*cm, 7.7*cm]))
    story.append(PageBreak())

    # ══════════════════════════════════
    # RESUMEN EJECUTIVO
    # ══════════════════════════════════
    story.append(h1("Resumen Ejecutivo  -  On-Premise vs AWS Cloud"))
    story.append(bd(
        "La siguiente tabla resume la comparativa entre la infraestructura local actual "
        "y la solucion propuesta en AWS, destacando los beneficios cuantificables para "
        "la empresa de transporte:"))
    story.append(sp(5))
    comp2 = [
        ["Aspecto", "Infraestructura On-Premise Actual", "Solucion AWS Propuesta"],
        ["Disponibilidad", "~95-97%%  (fallas hardware)", "99.99%%  (SLA garantizado AWS)"],
        ["Escalado", "Manual  (comprar nuevo hardware)", "Automatico en minutos"],
        ["Costos", "CAPEX alto  (HW, licencias, espacio)", "OPEX por uso  (solo lo que se usa)"],
        ["Respaldos", "Manuales a NAS local (riesgo)", "Automaticos, multi-region, inmutables"],
        ["Seguridad", "Firewall fisico, sin cifrado reposo", "IAM, MFA, KMS, SG, VPN, CloudTrail"],
        ["Recuperacion ante desastre", "Dias o semanas", "Minutos  (Multi-AZ + CRR)"],
        ["Monitoreo", "Limitado o inexistente", "CloudWatch 24/7 con alarmas automaticas"],
        ["Acceso remoto sucursales", "VPN lenta, dependiente de HW", "AWS Direct Connect o VPN gestionada"],
        ["Mantenimiento", "Equipo TI interno dedicado", "AWS gestiona hardware, SO RDS, parches"],
        ["Tiempo de despliegue", "Semanas o meses", "Horas o dias con IaC (Terraform/CDK)"],
    ]
    story.append(mk_table(comp2, [3.5*cm, 6*cm, 6.7*cm]))
    story.append(sp(8))

    story.append(h2("Proximos Pasos Recomendados"))
    for p in [
        "Fase 1  (Semanas 1-2): Configurar VPC, subnets, IGW, NAT GW y Security Groups en AWS.",
        "Fase 2  (Semanas 3-4): Lanzar instancias EC2, instalar agente CloudWatch, configurar EBS.",
        "Fase 3  (Semanas 5-6): Crear bucket S3, politicas IAM, tabla DynamoDB y migrar archivos.",
        "Fase 4  (Semanas 7-8): Configurar RDS, ejecutar AWS DMS para replicar SQL Server en vivo.",
        "Fase 5  (Semana 9): Pruebas de conectividad, checksums de datos, pruebas de carga con JMeter.",
        "Fase 6  (Semana 10): Cutover final, redireccion DNS, monitoreo intensivo 72 horas post-migracion.",
        "Post-migracion: Capacitacion del equipo TI en AWS, revision de costos mensual con Cost Explorer.",
    ]:
        story.append(bp(p))
    story.append(sp(8))

    story.append(h2("KPIs de Exito de la Migracion"))
    kpi_data = [
        ["KPI", "Objetivo", "Herramienta de Medicion"],
        ["Disponibilidad del sistema ERP", ">= 99.9%% mensual", "CloudWatch Availability"],
        ["Tiempo de respuesta ERP", "< 2 segundos", "CloudWatch + X-Ray"],
        ["RPO (Recovery Point Objective)", "< 1 hora", "RDS PITR + S3 Versioning"],
        ["RTO (Recovery Time Objective)", "< 15 minutos", "Multi-AZ RDS Failover"],
        ["Reduccion de costos IT", ">= 30%% vs CAPEX anual", "AWS Cost Explorer"],
        ["Incidentes de seguridad", "0 accesos no autorizados", "CloudTrail + GuardDuty"],
        ["Integridad de datos migrados", "100%%  checksum validado", "AWS DMS validation"],
    ]
    story.append(mk_table(kpi_data, [5*cm, 3.8*cm, 7.4*cm]))
    story.append(sp(10))
    story.append(nb(
        "La migracion a AWS representa una transformacion estrategica para la empresa de "
        "transporte: de una infraestructura rigida y costosa de mantener, a una plataforma "
        "elastica con disponibilidad de nivel bancario, seguridad avanzada y capacidad de "
        "respuesta inmediata ante el crecimiento del negocio nacional e internacional."))

    # BUILD body
    doc.build(story, onFirstPage=page_cb, onLaterPages=page_cb)
    body_buf.seek(0)

    # ── Merge cover + body
    out = "/home/null/core_portable/Documents/Code/University_clases/DevOps/act_4/docs/Equipo_5_Diagrama_Arquitectonico.pdf"
    writer = PdfWriter()
    for src in [cover_buf, body_buf]:
        reader = PdfReader(src)
        for page in reader.pages:
            writer.add_page(page)
    with open(out, "wb") as f:
        writer.write(f)
    print(f"PDF generado: {out}")

build()
