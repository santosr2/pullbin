#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pullbin import Pullbin

import os, re, sys, argparse

def interactive():
    try:
        pullbin = Pullbin()
        pullbin._show()
        domain = input("Set domain [default=pastebin]: ") or 'pastebin'
        try:
            if domain is not None and pullbin.check_domain(domain):
                pullbin.set_domain(domain)
        except Exception as excpt:
            print(f"Domain Value ERROR: {excpt}")
            sys.exit(2)

        key = input("Enter URI key [tips: https://pastebin.com/<KEY>]: ")
        if key == "":
            print("Need set key")
            sys.exit(1)

        try:
            if not pullbin.check_key(key):
                print("Check key unknow error")
        except Exception as excpt:
            print(f"Key Value ERROR: {excpt}")
            sys.exit(2)

        pwd = pullbin.get_current_path()
        filepath = input(f"Enter path [default={pwd}]: ") or pwd
        try:
            responseType = pullbin.set_path(filepath)
            if responseType == pullbin.ResponseType.IsFilePath:
                pass
            elif responseType == pullbin.ResponseType.IsDirPath:
                filename = key
                enterFileName = input("Do you want to enter filename? [y/N]: ") or "n"
                if re.match(r"(y|Y)(?:ES|es)?", enterFileName):
                    filename = input(f"Set filename [current={filename}]: ") or filename

                pullbin.set_filename(filename)
        except Exception as excpt:
            print(f"Path Valeu ERROR: {excpt}")

        try:
            pullbin.scrap_content()
        except Exception as excpt:
            print(f"Scrap ERROR: {excpt}")

        try:
            pullbin.write()
        except (IOError, TypeError) as error:
            print(f"Write ERROR: {error}")
        finally:
            pullbin.close()
    
    except KeyboardInterrupt:
        print("Finish with signal")

def cli():
    parser = argparse.ArgumentParser(prog="pullbin", description="Download artifacts from the Pastebin or Ghostbin")
    parser.add_argument("-d", "--domain", dest="domain", default="pastebin", required=False, help="Set domain [default=pastebin]")
    parser.add_argument("-k", "--key", dest="key", required=True, help="Set key [i.e: https://pastebin.com/<Key>]")
    parser.add_argument("-p", "--path", dest="path", default="", required=False, help="Set path for storage")
    parser.add_argument("-f", "--filename", dest="filename", default="", required=False, help="Set file name [default=<KEY>]")
    args = parser.parse_args()

    pullbin = Pullbin()
    pullbin._show()

    if not args.path:
        pullbin.fullpath = pullbin.get_current_path()
    else:
        pullbin.fullpath = os.path.basename(args.path)

    try:
        if pullbin.check_domain(args.domain):
            pullbin.set_domain(args.domain)
    except Exception as excpt:
        print(f"Domain Value ERROR: {excpt}")
        sys.exit(2)

    try:
        if not pullbin.check_key(args.key):
            print("Check key unknow error")
    except Exception as excpt:
        print(f"Key Value ERROR: {excpt}")
        sys.exit(2)
        
    if not args.filename:
        pullbin.set_filename(args.key)
    else:
        pullbin.set_filename(args.filename)

    try:
        pullbin.scrap_content()
    except Exception as excpt:
        print(f"Scrap ERROR: {excpt}")

    try:
        pullbin.write()
    except (IOError, TypeError) as error:
        print(f"Write ERROR: {error}")
    finally:
        pullbin.close()

if os.getenv("DOCKERNIZED"): # only for container mode
    from flask import Flask, request as apirequest, jsonify, Response

    app = Flask(__name__)
    
    if os.getenv("DEBUG"):
        app.config["DEBUG"] = True

    def getResponse(type_message, status, message):
        if status == 200:
            status_response = "200 OK"
        elif status == 500:
            status_response = "500 InternalServerError"
        elif status == 400:
            status_response = "400 BadGateway"
        elif status == 404:
            status_response = "404 NotFound"

        msg = '{"%s": {"status": %d, "message": "%s"}}' % (type_message, status, message)
        return Response(status=status_response, headers={
            "Content-Type": "application/json",
            "Content-Length": str(len(msg))
        })

    @app.route("/", methods=["POST"])
    def home():
        request_json = apirequest.get_json()

        if not 'key' in request_json:
            return jsonify({"error": "Need set key"})

        pullbin = Pullbin()

        pullbin.fullpath = "/data"

        try:
            if 'domain' in request_json and pullbin.check_domain(request_json['domain']):
                pullbin.set_domain(request_json['domain'])
        except Exception as excpt:
            return getResponse("error", 500, f'Domain Value ERROR: {excpt}')

        try:
            if not pullbin.check_key(request_json['key']):
                print("Check key unknow error")
        except Exception as excpt:
            return getResponse("error", 404, f'Key Value ERROR: {excpt}')
            
        if not 'filename' in request_json:
            pullbin.set_filename(request_json['key'])
        else:
            pullbin.set_filename(request_json['filename'])

        try:
            pullbin.scrap_content()
        except Exception as excpt:
            return getResponse("error", 500, f'Scrap ERROR: {excpt}')

        try:
            pullbin.write()
        except (IOError, TypeError) as error:
            pullbin.close()
            return getResponse("error", 500, f'Write ERROR: {error}')

        return getResponse("success", 200, "finish processing with success")

    @app.errorhandler(404)
    def page_notFound(e):
        return getResponse("error", 404, f'{e}')

    @app.errorhandler(400)
    def page_badGateway(e):
        return getResponse("error", 400, f'{e}')

    @app.errorhandler(500)
    def page_internalError(e):
        return getResponse("error", 500, f'{e}')


if __name__ == "__main__":
    if len(sys.argv[1:]):
        cli()
    else:
        interactive()