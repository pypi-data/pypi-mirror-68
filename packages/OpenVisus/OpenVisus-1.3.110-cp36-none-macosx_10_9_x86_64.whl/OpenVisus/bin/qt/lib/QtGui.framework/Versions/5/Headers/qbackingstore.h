/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtGui module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 2.0 or (at your option) the GNU General
** Public license version 3 or any later version approved by the KDE Free
** Qt Foundation. The licenses are as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-2.0.html and
** https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

#ifndef QBACKINGSTORE_H
#define QBACKINGSTORE_H

#include <QtGui/qtguiglobal.h>
#include <QtCore/qrect.h>

#include <QtGui/qwindow.h>
#include <QtGui/qregion.h>

QT_BEGIN_NAMESPACE


class QRegion;
class QRect;
class QPoint;
class QImage;
class QBackingStorePrivate;
class QPlatformBackingStore;

class Q_GUI_EXPORT QBackingStore
{
public:
    explicit QBackingStore(QWindow *window);
    ~QBackingStore();

    QWindow *window() const;

    QPaintDevice *paintDevice();

    // 'window' can be a child window, in which case 'region' is in child window coordinates and
    // offset is the (child) window's offset in relation to the window surface.
    void flush(const QRegion &region, QWindow *window = Q_NULLPTR, const QPoint &offset = QPoint());

    void resize(const QSize &size);
    QSize size() const;

    bool scroll(const QRegion &area, int dx, int dy);

    void beginPaint(const QRegion &);
    void endPaint();

    void setStaticContents(const QRegion &region);
    QRegion staticContents() const;
    bool hasStaticContents() const;

    QPlatformBackingStore *handle() const;

private:
    QScopedPointer<QBackingStorePrivate> d_ptr;
};

QT_END_NAMESPACE

#endif // QBACKINGSTORE_H
